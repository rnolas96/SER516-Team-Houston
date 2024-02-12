import logo from './logo.svg';
import './App.css';
import Hero from './components/Hero.js';
import SidebarMenu from './components/SidebarMenu.js';
import Burndown from './components/Burndown.js';
import LeadTime from './components/LeadTime.js';
import CycleTime from './components/CycleTime.js';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {

  // use the authtoke below to make sure that only the Hero page is
  // accessible until the authToken is available { @rkhatta1 }

  // Testing Stuff: 
  // window.onbeforeunload = function() {
  //   localStorage.clear();
  // }


  const authToken = localStorage.getItem('authToken');
  console.log(authToken);

  return (
    <div className="container-full">
      <Router>
          <Routes>
            <Route exact path="/" element={<Hero />} />
            <Route exact path="/burndowncharts" element={<Burndown />} />
            <Route exact path="/cycletime" element={<CycleTime />} />
            <Route exact path="/leadtime" element={<LeadTime />} />
          </Routes>
      </Router>
    </div>
  );
}

export default App;
