import './App.css';
import CycleTime from './components/CycleTime.js';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
function App() {

  const authToken = localStorage.getItem('authToken');
  console.log(authToken);

  return (
    <div className="container-full">
      <Router>
          <Routes>
            <Route exact path="/cycletime" element={<CycleTime />} />
          </Routes>
      </Router>
    </div>
  );
}

export default App;
