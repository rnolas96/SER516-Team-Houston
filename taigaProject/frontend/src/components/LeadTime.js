import React, { useEffect, useState } from 'react'
import '../App.css'
import SidebarMenu from './SidebarMenu'
import axios from 'axios'
import BarChartMaker from './reusable_components/BarChartMaker';


export default function LeadTime() {
const [averageLeadTimeData, setAverageLeadTimeData] = useState(null);
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
        text: "LeadTime data",
        datasets: [{
          label: 'LeadTime',
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
    if(!averageLeadTimeData && authToken) {
      apiCall('/api/task/lead_time?project_id=1522285', setAverageLeadTimeData, authToken);
    }
  }, []);
  return (
    <div className='container-full'>
      <SidebarMenu />
      <div className='route-container'>
        <BarChartMaker props={averageLeadTimeData}/>
      </div>
    </div>
  )
}