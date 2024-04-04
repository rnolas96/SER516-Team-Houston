import './App.css';
import LeadTime from './components/LeadTime.js';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
function App() {

  const authToken = localStorage.getItem('authToken');
  console.log(authToken);

  return (
    <div className="container-full">
      <Router>
          <Routes>
            <Route exact path="/leadtime" element={<LeadTime />} />
          </Routes>
      </Router>
    </div>
  );
}

export default App;
