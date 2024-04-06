import './App.css';
import CostOfDelay from './components/CostOfDelay.js';

function App() {

  const authToken = localStorage.getItem('authToken');
  console.log(authToken);

  return (
    <div className="container-full">
      <CostOfDelay/>
    </div>
  );
}

export default App;
