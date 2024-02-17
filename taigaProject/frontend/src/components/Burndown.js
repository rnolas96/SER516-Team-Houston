import React from 'react'
import axios from 'axios';
import { useEffect, useState } from 'react'
import '../App.css'
import LineChartMaker from './reusable_components/LineChartMaker'
import SidebarMenu from './SidebarMenu';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';
import {Buffer} from 'buffer';

export default function Burndown() {

  const [storyPointBurnDownData, setStoryPointBurnDownData] = useState(null);
  const [businessValueBurnDownData, setBusinessValueBurnDownData] = useState(null);
  const [taskBurnDownData, setTaskBurnDownData] = useState(null);

  function apiCall(url, updateCall, authToken) {
    axios.get(url, {
      headers: {
        'Authorization': authToken
      }}
    )
    .then(res => {

      const labels = Object.keys(res.data[0]);
      labels[0] = "";

      const updated = {
        labels: labels,
        text: "Burndown data of business value against sprints",
        datasets: [{
          label: 'Example burndown data',
          data: Object.values(res.data[0]),
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
          ],
          hoverOffset: 4
        }]
      }
    
      console.log("comes here");
      updateCall(updated);
    }
    );
  }

  useEffect (() => {

    const authToken = localStorage.getItem('authToken');
    console.log("authToken", authToken);

    if(!businessValueBurnDownData && authToken)  {
      // apiCall('/api/business_value_burndown?project_id=1522285', setBusinessValueBurnDownData, authToken);
    }

    if(!storyPointBurnDownData && authToken) {
      apiCall('/api/userstory/userstory_burndown?project_id=1522285', setStoryPointBurnDownData, authToken);
    }
    if(!taskBurnDownData && authToken) {
      // apiCall('/api/business_value_burndown?project_id=1522285', setBusinessValueBurnDownData, authToken);
    }

  }, []);

  return (
    <div className='container-full bg-gradient-to-r from-[#00f9f9] to-[#ffffff]'>
      <div className='route-container'>
        <Tabs>
          <TabList style={{display: 'flex', justifyContent: "space-between"}}>
            <Tab>Story-Points vs Sprints</Tab>
            <Tab>Business Value vs Sprints</Tab>
            <Tab>Tasks vs Sprints</Tab>
          </TabList>

          <TabPanel>
            <LineChartMaker props = {storyPointBurnDownData}/>
          </TabPanel>
          <TabPanel>
            <LineChartMaker props = {businessValueBurnDownData}/>
          </TabPanel>
          <TabPanel>
            <LineChartMaker props = {taskBurnDownData}/>
          </TabPanel>
        </Tabs>
      </div>
    </div>
  )
}
