import React, { useEffect, useState } from 'react'
import '../App.css'
import SidebarMenu from './SidebarMenu'
import axios from 'axios'
import BarChartMaker from './reusable_components/BarChartMaker';

export default function CycleTime() {

  const [averageCycleTimeLabels, setAverageCycleTimeLabels] = useState([]);
  const [averageCycleTimeValues, setAverageCycleTimeValues] = useState([]);

  useEffect (() => {

    const labels = [];
    const values = [];

    const cycletimeUrl = "/api/cycletime";
    // const data = axios.get(cycletimeUrl).then(res => {
    //     res.data.map((key, value) => {
    //       labels.push(key);
    //       values.push(value);
    //   })
    // })
  }, []);  

  const data = {
    labels: [ 'Sprint1', 'Sprint2', 'Sprint3', 'Sprint4', 'Sprint5'],
    text: "Average cycle time for each sprint",
    datasets: [{
      data: [15, 12, 21, 13, 12, 16]
    }]
  };

  return (
    <div className='container-full bg-white'>
      <div className='route-container'>        
        <BarChartMaker props={data}/>
      </div>
    </div>
  )
}
