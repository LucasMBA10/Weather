from django.db import models

class UserEntity:
    def __init__(self, 
                 username, 
                 name = None, 
                 id=None , 
                 email=None ,
                 password = None) -> None:
        
        
        self.id = id
        self.name = name
        self.email = email
        self.username=username
        self.password = password