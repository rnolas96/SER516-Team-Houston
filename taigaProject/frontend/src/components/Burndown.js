import React from 'react'
import axios from 'axios';
import { useEffect, useState } from 'react'
import '../App.css'
import LineChartMaker from './reusable_components/LineChartMaker'
import commonApiCall from '../commons'
import SidebarMenu from './SidebarMenu';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';
import {Buffer} from 'buffer';

export default function Burndown() {

  const [businessValueBurnDownData, setBusinessValueBurnDownData] = useState(null);
  const [partialStoryPointBurnDownData, setPartialStoryPointBurnDownData] = useState(null);
  const [fullStoryPointBurnDownData, setFullStoryPointBurnDownData] = useState(null);

  const [projectSlug, setProjectSlug] = useState(null)
  const [sprintData, setSprintData] = useState([])

  const [selectedOption, setSelectedOption] = useState('');

  const [projectId, setProjectId] = useState(null)
  const [sprintId, setSprintId] = useState(null)

  const [showLoader, setShowLoader] = useState(false)

  const clearData = () => {
    setSprintData([])
    setSprintId(null)
    setBusinessValueBurnDownData(null)
    setPartialStoryPointBurnDownData(null)
    setFullStoryPointBurnDownData(null)
    setSelectedOption('')
    setShowLoader(false)
  }

  const handleDropdownChange = (e) => {
    setSelectedOption(e.target.value);
    console.log(e.target.value)
    setSprintId(e.target.value)
    setShowLoader(true)
  };

  function onChangeProjectSlug(event) {
    setProjectSlug(event.target.value)
    clearData()

  }

  function apiCall(url, updateCall, scenario, authToken) {

    axios.get(url, {
        headers: {
          'Authorization': authToken
        }}
    )
    .then(res => {

      console.log("res", res.data);
      const labels = Object.keys(res.data);
      const values = Object.values(res.data);
      setShowLoader(false)

      labels[0] = "";
      const updated = {
        labels: labels,
        text: "Burndown data for " + scenario,
        datasets: [{
          label: 'Burndown Data',
          data: values,
          borderColor: 'black',
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 205, 86)'
          ],
          hoverOffset: 4
        }]
      }
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
      let s_Data = result.data[p_id]
      console.log(s_Data)
      setProjectId(p_id)
      setSprintData(s_Data)
      setShowLoader(true)

    })
  }

  useEffect (() => {

    const callApis = () => {

      const authToken = localStorage.getItem('authToken');
      console.log("authToken", authToken);
      console.log("sprintId", sprintId)
      console.log("projectId", projectId)

      if(authToken && projectId && sprintId)  {
        apiCall(`/api/userstory/business_value_burndown?project_id=${projectId}&sprint_id=${sprintId}`, setBusinessValueBurnDownData, "business value", authToken);
      }
      if(authToken && sprintId) {
        apiCall(`/api/userstory/partial_userstory_burndown?sprint_id=${sprintId}`, setPartialStoryPointBurnDownData, "partial storypoints", authToken);
      }
      if(authToken && sprintId) {
        apiCall(`/api/userstory/userstory_burndown?sprint_id=${sprintId}`, setFullStoryPointBurnDownData, "full storypoints", authToken);
      }

    }

    callApis();

    const intervalId = setInterval(callApis, 30000);
    return () => clearInterval(intervalId);

  }, [sprintId, projectId]);

  return (
    <div className='container-full bg-gradient-to-r from-[#FFB32C] to-[#ffd12c]'>
      <div className='route-container'>
        <Tabs style={{display: "flex", justifyContent: "space-between", flexDirection:"column"}}>
          <TabList style={{display: 'flex', justifyContent: "space-between"}}>
            <Tab>Partial SP Burndown</Tab>
            <Tab>Full SP Burndown</Tab>
            <Tab>Business Value Burndown</Tab>
          </TabList>
          <div style={{display: "flex", flexDirection:"column", justifyContent: "space-between", width: "50%"}}>
            <span className='text-[1.2rem] font-bold font-sans'>Project Slug:</span>
            <input className='bg-white border-2 rounded-xl hover:rounded-none duration-300 border-black h-[2.3rem] px-3 text-[1rem] font-sans' type='username' value={projectSlug} onChange={onChangeProjectSlug} aria-label='username' style={{marginBottom: "20px"}}/>
            <button className=' p-4 border-4 border-blue-950 hover:bg-blue-950 duration-300 hover:text-white font-sans font-bold rounded-2xl hover:rounded-none' onClick = {() => setProjectDetails()}>Submit</button>
            {sprintData.length > 0?
              <select value={selectedOption} onChange={handleDropdownChange} style={{marginTop: "10px"}}>
                <option value="">Select an option</option>
                {sprintData.map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.name}
                  </option>
                ))}
              </select> : null }
          </div>
           <TabPanel>
              <LineChartMaker data = {partialStoryPointBurnDownData} showLoader={showLoader}/> 
          </TabPanel>
          <TabPanel>
              <LineChartMaker data = {fullStoryPointBurnDownData} showLoader={showLoader}/>
          </TabPanel>
          <TabPanel>
              <LineChartMaker data = {businessValueBurnDownData} showLoader={showLoader}/>
          </TabPanel>

        </Tabs>
      </div>
    </div>
  )
}
