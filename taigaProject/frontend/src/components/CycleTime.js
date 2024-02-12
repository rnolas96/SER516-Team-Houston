import React, { useEffect, useState } from 'react'
import '../App.css'
import SidebarMenu from './SidebarMenu'
import axios from 'axios'
import BarChartMaker from './reusable_components/BarChartMaker';
export default function CycleTime() {


const [averageCycleTimeData, setAverageCycleTimeData] = useState(null);
  function apiCall(url, updateCall, authToken) {
    axios.get(url, {
      headers: {
        'Authorization': authToken
      }}
    )
    .then(res => {
      console.log(res.data)
      const labels = Object.keys(res.data);
      console.log("something")
      const updated = {
        labels: labels,
        text: "CycleTime data",
        datasets: [{
          label: 'Example CycleTime',
          data: Object.values(res.data),
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
          ],
          hoverOffset: 4
        }]
      }
      console.log("comes here", updated);
      updateCall(updated);
    }
    );
  }
  
  useEffect (() => {
    const authToken = localStorage.getItem('authToken');
    console.log("authToken", authToken);
    if(!averageCycleTimeData && authToken) {
      apiCall('/api/task/cycle_time?project_id=1522285', setAverageCycleTimeData, authToken);
    }
    
  }, []);
  
  return (
    <div className='container-full'>
      <SidebarMenu />
      <div className='route-container'>
        <BarChartMaker props={averageCycleTimeData}/>
      </div>
    </div>
  )
}