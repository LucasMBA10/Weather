from django.shortcuts import render, redirect
from django.views import View
from .authenticationUser import authenticate, generateToken
from django.http import HttpResponse
from .userRepository import UserRepository

# Create your views here.
class UserToken(View):
    def get(self, request):
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            return HttpResponse(generateToken(user))
        return HttpResponse('User not authenticated')
        
class UserLogin(View):
    def get(self, request):
        return render(request, 'authentificationUser.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username, password)
        
        if user:
            token = generateToken(user)
            request.session['token'] = token  # Armazena o token na sessão
            return redirect('Weather View',user_id=user.id)
        return HttpResponse('User not authenticated')

class UserInsert(View):
    def get(self, request):
        return render(request, 'create_user.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        user_repo = UserRepository('users')  # 'users' é o nome da coleção no MongoDB
        
        # Verifica se o username já está em uso
        filter = {'username': username}
        existing_user = user_repo.get(filter)
        if existing_user:
            return render(request, 'create_user.html', {'error_message': 'Username already exists. Please choose a different one.'})
        
        # Cria o novo usuário
        user_repo.insert({
            'username': username,
            'password': password,
            'email': email
        })
        return redirect('User Login')

class UserForget(View):
    def get(self, request):
        return render(request, 'forgot_password.html')

class UserEdit(View):
    def get(self, request, user_id):
        user_repo = UserRepository('users')
        user = user_repo.getByID(user_id)
        if not user:
            return HttpResponse('User not found', status=404)
        
        return render(request, 'edit_user.html', {'user': user, 'user_id': user_id})


    def post(self, request, user_id):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        user_repo = UserRepository('users')
        user = user_repo.getByID(user_id)
        if not user:
            return HttpResponse('User not found', status=404)
        
        user_repo.update({
            'username': username,
            'password': password,
            'email': email
        }, user_id)
        return redirect('User Login')

class UserDelete(View):
    def get(self, request, user_id):
        user_repo = UserRepository('users')
        user = user_repo.getByID(user_id)
        if not user:
            return HttpResponse('User not found', status=404)
        
        return render(request, 'confirm_delete_user.html', {'user': user})

    def post(self, request, user_id):
        user_repo = UserRepository('users')
        user_repo.deleteByID(user_id)
        return HttpResponse('User deleted successfully')

