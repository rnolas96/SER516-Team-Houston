import React, { useEffect, useState } from 'react'
import '../App.css'
import SidebarMenu from './SidebarMenu'
import axios from 'axios'
import BarChartMaker from './reusable_components/BarChartMaker';
export default function Engagement() {

const [engagementData, setEngagementData] = useState(null);
  function apiCall(url, updateCall, authToken) {
    // axios.get(url, {
    //   headers: {
    //     'Authorization': authToken
    //   }}
    // )
    // .then(res => {
    //   console.log(res.data)
    //   const labels = Object.keys(res.data);

      const engagementLabels = ["commits", "task activity", "pull requests", "something else 1", "something else 2"]
      const engagementValues = [10, 20, 13, 55, 14];

      console.log("something")
      const updated = {
        labels: engagementLabels,
        text: "Engagement data",
        datasets: [
          {
            label: "Sprint 1",
            data: engagementValues,
            backgroundColor: [
                'rgb(255, 99, 132)'
            ],
            hoverOffset: 4
          },
          {
            label: "Sprint 2",
            data: engagementValues,
            backgroundColor: [
                'rgb(54, 132, 99)'
            ],
            hoverOffset: 4
          },
          {
            label: "Sprint 3",
            data: engagementValues,
            backgroundColor: [
                'rgb(99, 132, 255)'
            ],
            hoverOffset: 4
          },
          {
            label: "Sprint 4",
            data: engagementValues,
            backgroundColor: [
                'rgb(99, 99, 54)'
            ],
            hoverOffset: 4
          },
          {
            label: "Sprint 5",
            data: engagementValues,
            backgroundColor: [
                'rgb(132, 132, 132)'
            ],
            hoverOffset: 4
          },
        ]
      }
      console.log("comes here", updated);
      updateCall(updated);
    // }
    // );
  }
  
  useEffect (() => {
    const authToken = localStorage.getItem('authToken');
    console.log("authToken", authToken);
    if(!engagementData && authToken) {
      apiCall('/api/engagement/engagement_data?project_id=1522285', setEngagementData, authToken);
    }
    
  }, []);
  
  return (
    <div className='container-full'>
      <div className='route-container'>
        <BarChartMaker props={engagementData}/>
      </div>
    </div>
  )
}