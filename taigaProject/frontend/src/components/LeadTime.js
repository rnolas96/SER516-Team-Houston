import React, { useEffect, useState } from 'react'
import '../App.css'
import SidebarMenu from './SidebarMenu'
import axios from 'axios'
import BarChartMaker from './reusable_components/BarChartMaker';
import { Box } from '@ant-design/plots';

export default function LeadTime() {
  
const [leadTimeData, setLeadTimeData] = useState([]);
  function apiCall(url, updateCall, authToken) {
    axios.get(url, {
      headers: {
        'Authorization': authToken
      }}
    )
    .then(res => {
      let sprintData = []

      if (res.data) { // Only proceed if res.data exists
        const data = Object.entries(res.data).reduce((acc, [sprint, tasks]) => {
          acc[sprint] = acc[sprint] || [];
          acc[sprint].push(...tasks.map(task => task.lead_time));
          return acc;
        }, {});
        // Convert the object to an array of sprints with cycle time arrays
        sprintData = Object.entries(data).map(([x, y]) => ({
          x,
          y
        }));
        console.log("sprintData", sprintData);
      } else {
        console.error("res.data is undefined. Cannot process data.");
      }
      console.log("sprintData", sprintData);

      const hasLongList = sprintData.some(item => item.y.length >= 5);

      console.log("hasLongList", hasLongList);

      // let sprintData = [
      //   { x: 'Sprint1', y : [1, 9, 16, 22, 24]},
      //   { x: 'Sprint2', y : [2, 8, 12, 21, 28]},
      //   { x: 'Sprint3', y : [1, 7, 10, 17, 22]}
      // ]

      let updated = {
        height: 600,
        width: 600,
        autoFit: false,
        inset: 8,
        data: {
          value: sprintData
        },
        // boxType: 'boxplot',
        boxStyle: {
          stroke: '#545454',
          fill: '#1890FF',
          fillOpacity: 0.3,
        },
        xField: 'x',
        yField: 'y',
        point: {
          size: 5,
          shape: 'point',
        },
        tooltip: {
          items: [
            { name: 'Lead Time (Days)', channel: 'y' }
          ],
        },
        axis: { y: { tickCount: 2 } },
        // coordinate: { transform: [{ type: 'transpose' }] },
        style: { boxFill: 'red', pointStroke: 'white' },
      }

      if(!hasLongList)
        updated['boxType'] = 'boxplot'

      updateCall(updated);
    }
    );
  }
  
  useEffect (() => {
    const authToken = localStorage.getItem('authToken');
    console.log("authToken", authToken);
    if(!leadTimeData.length && authToken) {
      apiCall('/api/task/lead_time?project_id=1522285', setLeadTimeData, authToken);
    }    
  }, []);
  
  return (
    <div className='container-full'>
      <SidebarMenu />
      <div className='route-container'>
        {leadTimeData &&
           <Box {...leadTimeData} />}
      </div>
    </div>
  )
}