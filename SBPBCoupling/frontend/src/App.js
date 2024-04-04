import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SbpbCoupling from './components/SbpbCoupling';
function App() {

  const authToken = localStorage.getItem('authToken');
  console.log(authToken);

  return (
    <div className="container-full">
      <Router>
          <Routes>
            <Route exact path="/sbpbcoupling" element={<SbpbCoupling />} />
          </Routes>
      </Router>
    </div>
  );
}

export default App;
