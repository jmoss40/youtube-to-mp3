import './App.css';
import Converter from './components/Converter';
import Footer from './components/Footer';
import DarkModeToggle from './components/DarkModeToggle';

function App() {
  return <div className="App">
    <div className="App-header">
      <DarkModeToggle/>
      <Converter/>
      <Footer/>
    </div>
  </div>
}

export default App;
