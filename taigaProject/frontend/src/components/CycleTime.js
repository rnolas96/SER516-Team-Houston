import React, { useEffect, useState, useRef } from 'react'
import '../App.css'
import SidebarMenu from './SidebarMenu'
import axios from 'axios'
import BarChartMaker from './reusable_components/BarChartMaker';
import { Box } from '@ant-design/plots';

export default function CycleTime() {

  const [cycleTimeData, setCycleTimeData] = useState({});
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
          acc[sprint].push(...tasks.map(task => task.cycle_time));
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
            { name: 'Cycle Time (Days)', channel: 'y' }
          ],
        },
        axis: { y: { tickCount: 2 } },
        // coordinate: { transform: [{ type: 'transpose' }] },
        style: { boxFill: 'red', pointStroke: 'white' },
      }

      if(!hasLongList)
        updated['boxType'] = 'boxplot'

      setCycleTimeData(updated);
    });
  }
  useEffect (() => {
    const authToken = localStorage.getItem('authToken');
    console.log("authToken", authToken);
    if(!cycleTimeData.length && authToken) {
      apiCall('/api/task/cycle_time?project_id=1521718', setCycleTimeData, authToken);
    }
    
  }, []);
  
  return (
    <div className='container-full'>
      <SidebarMenu />
      <div className='route-container'>
      {/* <span className='text-[1.2rem] font-bold font-sans'>Project Slug:</span>
        <input className='bg-white border-2 rounded-xl hover:rounded-none duration-300 border-black h-[2.3rem] px-3 text-[1rem] font-sans' type='username' value={projectSlug} onChange={onChangeProjectSlug} aria-label='username' style={{marginBottom: "20px"}}/>
         */}
        {cycleTimeData &&
           <Box {...cycleTimeData} />}
         
        {/* <BarChartMaker props={averageCycleTimeData}/> */}
      </div>
    </div>
  )
}

// const updated = {
      //   height: 500,
      //   width: 100,
      //   autoFit: true,
      //   inset: 8,
      //   data: {
      //     value: res.data[]
      //   },
      //   boxType: 'boxplot',
      //   xField: 'sprint 1',
      //   yField: 'lead_time',
      //   point: {
      //     size: 5,
      //     shape: 'point',
      //   },
      //   tooltip: {
      //     items: [
      //       { name: 'Lead Time (Days)', channel: 'y' }        
      //     ],
      //   },
      //   // coordinate: { transform: [{ type: 'transpose' }] },
      //   style: { boxFill: 'red', pointStroke: 'white' },
      // }
    
      // console.log("comes here", updated);
      // updateCall(updated);


      // const data = [
      //   { x: 'Oceania', y: [1, 9, 16, 22, 24] },
      //   { x: 'East Europe', y: [1, 5, 8, 12, 16] },
      //   { x: 'Australia', y: [1, 8, 12, 19, 26] },
      //   { x: 'South America', y: [2, 8, 12, 21, 28] },
      //   { x: 'North Africa', y: [1, 8, 14, 18, 24] },
      //   { x: 'North America', y: [3, 10, 17, 28, 30] },
      //   { x: 'West Europe', y: [1, 7, 10, 17, 22] },
      //   { x: 'West Africa', y: [1, 6, 8, 13, 16] },
      // ];
    
      // const config = {
      //   data: {
      //     value: data,
      //   },
      //   xField: 'x',
      //   yField: 'y',
      //   colorField: 'x',
      //   scale: { x: { paddingInner: 0.6, paddingOuter: 0.3 }, y: { zero: true } },
      //   coordinate: { type: 'polar', innerRadius: 0.2 },
      //   style: { stroke: 'black' },
      //   axis: { y: { tickCount: 5 } },
      //   legend: false,
      // };
      // return <Box {...config} />;