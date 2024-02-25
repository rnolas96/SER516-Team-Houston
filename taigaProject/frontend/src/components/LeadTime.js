import React, { useEffect, useState, useRef } from 'react'
import '../App.css'
import SidebarMenu from './SidebarMenu'
import axios from 'axios'
import BarChartMaker from './reusable_components/BarChartMaker';
import BoxPlotChartMaker from './reusable_components/BoxPlotChartMaker';

export default function LeadTime() {
  
  const [leadTimeData, setLeadTimeData] = useState([]);
  const [projectSlug, setProjectSlug] = useState(null);
  const [projectId, setProjectId] = useState(null)

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

      console.log(res.data)

      let data = res.data;

      // let sprintData = [
      //   { x: 'Sprint1', y : [1, 9, 16, 22, 24]},
      //   { x: 'Sprint2', y : [2, 8, 12, 21, 28]},
      //   { x: 'Sprint3', y : [1, 7, 10, 17, 22]}
      // ]

      const leadTimeValuesByKey = {};

      for (const key in data) {
        leadTimeValuesByKey[key] = data[key].map(item => item['lead_time']);
      }
      
      let labels = Object.keys(leadTimeValuesByKey);
      let values = Object.values(leadTimeValuesByKey);
      

      let updated = {
        labels: labels,
        values: values
      };

      updated["label"] = "Boxplot";


      updateCall(updated);
    }
    );
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
    if(!leadTimeData.length && authToken && projectId) {
      apiCall(`/api/task/lead_time?project_id=${projectId}`, setLeadTimeData, authToken);
    }    
  }, [projectId]);
  
  return (
    <div className='container-full'>
      <div className='route-container' style={{display: "flex", flexDirection:"column", justifyContent: "space-between"}}>
        <div style={{marginTop: 50,  display: "flex", flexDirection:"column"}}>
          <span className='text-[1rem] mb-[0.3rem] font-bold font-sans'>Project Slug:</span>
          <input className='bg-white border-2 rounded-xl hover:rounded-md duration-300 border-[#ffd053] h-[2.3rem] px-3 text-[1rem] font-sans' type='username' value={projectSlug} onChange={onChangeProjectSlug} aria-label='username' style={{marginBottom: "20px"}}/>
          <button className=' p-4 border-4 border-[#ffd053] hover:bg-[#ffd053] duration-300 hover:text-white font-sans font-bold rounded-2xl hover:rounded-md' onClick = {() => setProjectDetails()}>Submit</button>
        </div>
        <div>
          {leadTimeData &&
            <BoxPlotChartMaker {...leadTimeData} />}
        </div>
      </div>
    </div>
  )
}