import './App.css';

import Burndown from './components/Burndown.js';

function App() {

  const authToken = localStorage.getItem('authToken');
  console.log(authToken);

  return (
    <div className="container-full">
      <Burndown/>
    </div>
  );
}

export default App;
