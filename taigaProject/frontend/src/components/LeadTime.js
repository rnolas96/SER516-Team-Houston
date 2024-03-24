import React, { useEffect, useState, useRef } from 'react'
import '../App.css'
import SidebarMenu from './SidebarMenu'
import axios from 'axios'
import BarChartMaker from './reusable_components/BarChartMaker';
import BoxPlotChartMaker from './reusable_components/BoxPlotChartMaker';
import Loader from './reusable_components/Loader';

export default function LeadTime() {
  
  const [leadTimeData, setLeadTimeData] = useState([]);
  const [projectSlug, setProjectSlug] = useState(null);
  const [projectId, setProjectId] = useState(null);
  const [showLoader, setShowLoader] = useState(false);

  const [rangedLeadTimeData, setRangedLeadTimeData] = useState({});
  const [startDate, setStartDate] = useState(new Date(2024, 1, 24)); // dummy values for testing @rkhatta
  const [endDate, setEndDate] = useState(new Date(2024, 2, 24)); // dummy values for testing @rkhatta

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
      let sprintData = []

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
      if (p_id != null) {
        setShowLoader(false)
      } else {
        setShowLoader(true)
      }

    })
  }
  
  useEffect (() => {
    const authToken = localStorage.getItem('authToken');
    if(projectId && startDate && endDate && authToken) {
      let formattedStartDate = startDate.toISOString().slice(0, 10);
      console.log("startdate", startDate, "    formattedStartDate", formattedStartDate);
      let formattedEndDate = endDate.toISOString().slice(0, 10);
      apiCall(`/api/task/lead_time_time_range?project_id=${projectId}&start_date=${formattedStartDate}&end_date=${formattedEndDate}`, setRangedLeadTimeData, authToken);
    }   
  }, [projectId]);
  
  return (
    <div className="container-full">
      <div
        className="flex flex-col min-h-[100%] justify-between w-[100%] pt-[1rem] pb-[1rem] px-[2rem]"
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            width: "50%",
            // minHeight: "50%"
          }}
          className="parent"
        >
          <div className="text-[2rem] w-auto rounded-none border-solid border-b-[4px] border-b-[#ffd053] font-bold bg-white hover:border-b-red-400 duration-300 font-sans text-start mt-0 pb-[0.2rem] mb-[1rem]">
            <span>Lead Time</span>
          </div>
          <span className="text-[1rem] font-bold font-sans">Project Slug:</span>
          <div className="flex flex-row justify-between h-[2.5rem] space-x-[0.8rem] mt-[0.3rem] mb-[0.6rem]">
            <input
              className="bg-white border-2 rounded-xl hover:rounded-none duration-300 border-[#ffd053] h-[2.3rem] px-3 w-[67%] text-[1rem] font-sans"
              type="username"
              value={projectSlug}
              onChange={onChangeProjectSlug}
              aria-label="username"
            />
            <button
              className="ml-[0.6rem] h-[2.45rem] w-[33%] border-4 border-[#ffd053] hover:bg-[#ffd053] duration-300 hover:text-white font-sans font-bold rounded-2xl hover:rounded-none"
              onClick={() => setProjectDetails()}
            >
              Submit
            </button>
          </div>
        </div>{" "}
        <div>
          {rangedLeadTimeData &&
            <BoxPlotChartMaker {...rangedLeadTimeData} />}
        </div>
      </div>
    </div>
  )
}