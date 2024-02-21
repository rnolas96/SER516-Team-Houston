import logo from './logo.svg';
import './App.css';
import Hero from './components/Hero.js';
import SidebarMenu from './components/SidebarMenu.js';
import Burndown from './components/Burndown.js';
import LeadTime from './components/LeadTime.js';
import CycleTime from './components/CycleTime.js';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { ProSidebarProvider } from 'react-pro-sidebar';
import Engagement from './components/Engagement.js';
// import CostOfDelay from './components/CostOfDelay.js';

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
            {/* <Route exact path="/costofdelay" element={<CostOfDelay/>} /> */}
            <Route exact path="/engagement" element={<Engagement/>} />
          </Routes>
      </Router>
    </div>
  );
}

export default App;
