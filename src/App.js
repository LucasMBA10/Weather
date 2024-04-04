import logo from './logo.svg';
import './App.css';
import Forecast from './components/Forecast/Forecast';
import Tempinfo from './components/TempInfo/TempInfo';
import Search from './components/Search/Search';


function App() {
  return (
    <div>
      <Search/>
      <Tempinfo/>
      <Forecast/>
      
    </div>
  );
}

export default App;