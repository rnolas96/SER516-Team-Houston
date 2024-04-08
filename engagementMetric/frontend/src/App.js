import './App.css';
import Engagement from './components/Engagement.js';
function App() {

  const authToken = localStorage.getItem('authToken');
  console.log(authToken);

  return (
    <div className="container-full">
      <Engagement/>
    </div>
  );
}

export default App;
