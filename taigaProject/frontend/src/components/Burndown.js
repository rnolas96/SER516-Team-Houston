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

  const [businessValueBurnDownData, setBusinessValueBurnDownData] = useState(null);
  const [partialStoryPointBurnDownData, setPartialStoryPointBurnDownData] = useState(null);
  const [fullStoryPointBurnDownData, setFullStoryPointBurnDownData] = useState(null);


  function doubleCheck(url, updateCall, scenario, authToken) {

    apiCall(url, updateCall, scenario, authToken)
    let count = 0
    setTimeout(() => {
      doubleCheck(url, updateCall, scenario, authToken)
    }, 30000)
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
      labels[0] = "";
      const updated = {
        labels: labels,
        text: "Burndown data for " + scenario,
        datasets: [{
          label: 'Burndown Data',
          data: values,
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 205, 86)'
          ],
          hoverOffset: 4
        }]
      }
        updateCall(updated);
      }
    );    
    
  }

  useEffect (() => {

    const authToken = localStorage.getItem('authToken');
    console.log("authToken", authToken);

    if(!businessValueBurnDownData && authToken)  {
      doubleCheck('/api/userstory/business_value_burndown?project_id=1521718&sprint_id=376612', setBusinessValueBurnDownData, "business value", authToken);
    }
    if(!partialStoryPointBurnDownData && authToken) {
      doubleCheck('/api/userstory/partial_userstory_burndown?sprint_id=376612', setPartialStoryPointBurnDownData, "partial storypoints", authToken);
    }
    if(!fullStoryPointBurnDownData && authToken) {
      doubleCheck('/api/userstory/userstory_burndown?sprint_id=376612', setFullStoryPointBurnDownData, "full storypoints", authToken);
    }

  }, []);

  return (
    <div className='container-full bg-gradient-to-r from-[#00f9f9] to-[#ffffff]'>
      <div className='route-container'>
        <Tabs>
          <TabList style={{display: 'flex', justifyContent: "space-between"}}>
            <Tab>Partial SP Burndown</Tab>
            <Tab>Full SP Burndown</Tab>
            <Tab>Business Value Burndown</Tab>
          </TabList>

          <TabPanel>
            <LineChartMaker props = {partialStoryPointBurnDownData}/>
          </TabPanel>
          <TabPanel>
            <LineChartMaker props = {fullStoryPointBurnDownData}/>
          </TabPanel>
          <TabPanel>
            <LineChartMaker props = {businessValueBurnDownData}/>
          </TabPanel>
        </Tabs>
      </div>
    </div>
  )
}
