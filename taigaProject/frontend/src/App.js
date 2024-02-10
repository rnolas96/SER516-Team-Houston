import logo from './logo.svg';
import './App.css';
import './components/ChartMaker'
import Hero from './components/Hero.js';
import SidebarMenu from './components/SidebarMenu.js';
import Burndown from './components/Burndown.js';
import LeadTime from './components/LeadTime.js';
import CycleTime from './components/CycleTime.js';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <>
    <Router>
      <div className='flex h-screen'>
      <SidebarMenu />
      <Routes>
        <Route exact path="/" element={<Hero />} />
        <Route exact path="/burndowncharts" element={<Burndown />} />
        <Route exact path="/cycletime" element={<CycleTime />} />
        <Route exact path="/leadtime" element={<LeadTime />} />
      </Routes>
      </div>
    </Router>
    
    </>
  );
}

export default App;
