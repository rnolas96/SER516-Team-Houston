import logo from './logo.svg';
import './App.css';
import TaskCoupling from './components/TaskCoupling.js';
function App() {

  const authToken = localStorage.getItem('authToken');
  console.log(authToken);

  return (
    <div className="container-full">
      <TaskCoupling />
    </div>
  );
}

export default App;
