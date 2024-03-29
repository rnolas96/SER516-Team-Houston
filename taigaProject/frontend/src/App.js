import logo from './logo.svg';
import './App.css';
import Hero from './components/Hero.js';
import SidebarMenu from './components/SidebarMenu.js';
import Burndown from './components/Burndown.js';
import LeadTime from './components/LeadTime.js';
import CycleTime from './components/CycleTime.js';
import SbpbCoupling from './components/SbpbCoupling.js';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { ProSidebarProvider } from 'react-pro-sidebar';
import CostOfDelay from './components/CostOfDelay.js';
import Engagement from './components/Engagement.js';
import TaskCoupling from './components/TaskCoupling.js';
function App() {

  const authToken = localStorage.getItem('authToken');
  console.log(authToken);

  return (
    <div className="container-full">
      <Router>
        <ProSidebarProvider>
          <SidebarMenu />
        </ProSidebarProvider>
          <Routes>
            <Route exact path="/" element={<Hero />} />
            <Route exact path="/burndowncharts" element={<Burndown />} />
            <Route exact path="/cycletime" element={<CycleTime />} />
            <Route exact path="/leadtime" element={<LeadTime />} />
            <Route exact path="/costofdelay" element={<CostOfDelay/>} />
            <Route exact path="/sbpbcoupling" element={<SbpbCoupling/>} />
            <Route exact path="/engagement" element={<Engagement/>} />
            <Route exact path="/taskcoupling" element={<TaskCoupling/>} />
          </Routes>
      </Router>
    </div>
  );
}

export default App;
