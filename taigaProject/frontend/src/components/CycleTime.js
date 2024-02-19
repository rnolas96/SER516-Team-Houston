import React, { useEffect, useState, useRef } from 'react'
import '../App.css'
import SidebarMenu from './SidebarMenu'
import axios from 'axios'
import BarChartMaker from './reusable_components/BarChartMaker';
import { Box } from '@ant-design/plots';

export default function CycleTime() {

  const [projectSlug, setProjectSlug] = useState(null);
  const [projectId, setProjectId] = useState(null)
  const [cycleTimeData, setCycleTimeData] = useState({});

  function onChangeProjectSlug(event) {
    setProjectSlug(event.target.value)
  }

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

      updateCall(updated);
    });
  }

  function setProjectDetails() {
    const authToken = localStorage.getItem('authToken');
    let url = '/api/project/milestone_data?project_slug=' + projectSlug
    axios.get(url, {
      headers: {
          'Authorization': authToken
      }
    }).then(result => {
      console.log("result", result.data)
      console.log("p_id", Object.keys(result.data)[0])
      let p_id = Object.keys(result.data)[0]
      // let p_id = 1521718
      setProjectId(p_id)
    })
  }

  useEffect (() => {
    const authToken = localStorage.getItem('authToken');
    console.log("authToken", authToken);
    if(!cycleTimeData.length && authToken && projectId) {
      apiCall(`/api/task/cycle_time?project_id=${projectId}`, setCycleTimeData, authToken);
    }
  }, [projectId]);
  
  return (
    <div className='container-full'>
      <SidebarMenu />
      <div className='route-container' style={{display: "flex", flexDirection:"column", justifyContent: "space-between"}}>
        <div style={{marginTop: 50}}>
          <span className='text-[1.2rem] font-bold font-sans'>Project Slug:</span>
          <input className='bg-white border-2 rounded-xl hover:rounded-none duration-300 border-black h-[2.3rem] px-3 text-[1rem] font-sans' type='username' value={projectSlug} onChange={onChangeProjectSlug} aria-label='username' style={{marginBottom: "20px"}}/>
          <button className=' p-4 border-4 border-blue-950 hover:bg-blue-950 duration-300 hover:text-white font-sans font-bold rounded-2xl hover:rounded-none' onClick = {() => setProjectDetails()}>Submit</button>
        </div>
        <div>
          {cycleTimeData &&
            <Box {...cycleTimeData} />}
        </div>
      </div>
    </div>
  )
}