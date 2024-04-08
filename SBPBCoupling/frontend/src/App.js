import './App.css';
import SbpbCoupling from './components/SbpbCoupling';
function App() {

  const authToken = localStorage.getItem('authToken');
  console.log(authToken);

  return (
    <div className="container-full">
     
          <SbpbCoupling/>
        
    </div>
  );
}

export default App;
