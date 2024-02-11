import React from 'react'
import axios from 'axios';
import { useEffect, useState } from 'react'
import '../App.css'
import LineChartMaker from './reusable_components/LineChartMaker'
import SidebarMenu from './SidebarMenu';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';

export default function Burndown() {

  const [taskBurnDownData, setTaskBurnDownData] = useState(null);
  const [storyPointBurnDownData, setstoryPointBurnDownData] = useState(null);
  const [businessValueBurnDownData, setBusinessValueBurnDownData] = useState(null);

  const data1 = {
    labels: ['', 'Sprint1', 'Sprint2', 'Sprint3', 'Sprint4', 'Sprint5'],
    text: "Burndown data of story-points against sprints",
    datasets: [{
      label: 'Example burndown data',
      data: [15, 12, 9, 7, 5, 3],
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
      hoverOffset: 4
    }]
  };

  const data2 = {
    labels: ['', 'Sprint1', 'Sprint2', 'Sprint3', 'Sprint4', 'Sprint5'],
    text: "Burndown data of business value against sprints",
    datasets: [{
      label: 'Example burndown data',
      data: [15, 12, 9, 7, 5, 3],
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
      hoverOffset: 4
    }]
  };

  const data3 = {
    labels: ['', 'Sprint1', 'Sprint2', 'Sprint3', 'Sprint4', 'Sprint5'],
    text: "Burndown data of tasks against sprints",
    datasets: [{
      label: 'Example burndown data',
      data: [15, 12, 9, 7, 5, 3],
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
      hoverOffset: 4
    }]
  };

  useEffect (() => {

    // if(!taskBurnDownData)
    //   axios.get('/api').then(res => setTaskBurnDownData(res.data));

    // if(!storyPointBurnDownData)
    //   axios.get('/api').then(res => setstoryPointBurnDownData(res.data));

    // if(!taskBurnDownData)
    //   axios.get('/api').then(res => setBusinessValueBurnDownData(res.data));

  }, []);

  return (
    <div className='container-full'>
      <SidebarMenu />
      <div className='route-container'>
        <Tabs>
          <TabList style={{display: 'flex', justifyContent: "space-between"}}>
            <Tab>Story-Points vs Sprints</Tab>
            <Tab>Business Value vs Sprints</Tab>
            <Tab>Tasks vs Sprints</Tab>
          </TabList>

          <TabPanel>
            <LineChartMaker props = {data1}/>
          </TabPanel>
          <TabPanel>
            <LineChartMaker props = {data2}/>
          </TabPanel>
          <TabPanel>
            <LineChartMaker props = {data3}/>
          </TabPanel>
        </Tabs>
        <div>
          {/* <LineChartMaker props = {taskBurnDownData}/>
          <LineChartMaker props = {storyPointBurnDownData}/>
          <LineChartMaker props = {businessValueBurnDownData}/> */}
        </div>
      </div>
    </div>
  )
}
