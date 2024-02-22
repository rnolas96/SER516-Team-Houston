import React, { useEffect, useState } from 'react'
import '../App.css'
import SidebarMenu from './SidebarMenu'
import axios from 'axios'
import BarChartMaker from './reusable_components/BarChartMaker';
export default function Engagement() {

  const [engagementData, setEngagementData] = useState(null);

  const [projectSlug, setProjectSlug] = useState(null);
  const [sprintData, setSprintData] = useState([]);

  const [selectedOption, setSelectedOption] = useState("");

  const [projectId, setProjectId] = useState(null);
  const [sprintId, setSprintId] = useState(null);

  const [showLoader, setShowLoader] = useState(false);

  const clearData = () => {
    setSprintData([]);
    setSprintId(null);
    setEngagementData(null);
    setSelectedOption("");
    setShowLoader(false);
  };

  const handleDropdownChange = (e) => {
    setSelectedOption(e.target.value);
    console.log(e.target.value);
    setSprintId(e.target.value);
    setShowLoader(true);
  };

  function onChangeProjectSlug(event) {
    setProjectSlug(event.target.value);
    clearData();
  }

  function setProjectDetails() {
    const authToken = localStorage.getItem("authToken");
    let url = "/api/project/milestone_data?project_slug=" + projectSlug;

    axios
      .get(url, {
        headers: {
          Authorization: authToken,
        },
      })
      .then((result) => {
        console.log("result", result.data);
        console.log("p_id", Object.keys(result.data)[0]);

        let p_id = Object.keys(result.data)[0];
        let s_Data = result.data[p_id];
        console.log(s_Data);
        setProjectId(p_id);
        setSprintData(s_Data);
        setShowLoader(true);
      });
  }


  function apiCall(url, updateCall, authToken) {
    // axios.get(url, {
    //   headers: {
    //     'Authorization': authToken
    //   }}
    // )
    // .then(res => {
    //   console.log(res.data)
    //   const labels = Object.keys(res.data);

      const engagementLabels = ["commits", "task activity", "pull requests", "something else 1", "something else 2"]
      const engagementValues = [10, 20, 13, 55, 14];

      console.log("something")
      const updated = {
        labels: engagementLabels,
        text: "Engagement data",
        datasets: [
          {
            label: "Person 1",
            data: engagementValues,
            backgroundColor: [
                'rgb(255, 99, 132)'
            ],
            hoverOffset: 4
          },
          {
            label: "Person 2",
            data: engagementValues,
            backgroundColor: [
                'rgb(54, 132, 99)'
            ],
            hoverOffset: 4
          },
          {
            label: "Person 3",
            data: engagementValues,
            backgroundColor: [
                'rgb(99, 132, 255)'
            ],
            hoverOffset: 4
          },
          {
            label: "Person 4",
            data: engagementValues,
            backgroundColor: [
                'rgb(99, 99, 54)'
            ],
            hoverOffset: 4
          },
          {
            label: "Person 5",
            data: engagementValues,
            backgroundColor: [
                'rgb(132, 132, 0)'
            ],
            hoverOffset: 4
          },
        ]
      }
      console.log("comes here", updated);
      updateCall(updated);
    // }
    // );
  }
  
  useEffect (() => {

    const callApis = () => {
        const authToken = localStorage.getItem("authToken");
        console.log("authToken", authToken);
        console.log("sprintId", sprintId);
        console.log("projectId", projectId);
  
        if (authToken && projectId && sprintId) {
            apiCall('/api/engagement/engagement_data?project_id=1522285', setEngagementData, authToken);
        }
      };
  
      callApis();
      const intervalId = setInterval(callApis, 30000);
      return () => clearInterval(intervalId);
    
  }, [sprintId, projectId]);
  
  return (
    <div className='container-full'>
      <div className="route-container flex flex-col min-h-[100%]">
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
            <div>
            <span className="text-[1rem] font-bold font-sans">
              Project Slug:
            </span>
            </div>
            <div 
              style={{
                display: "flex",
                flexDirection: "row",
                justifyContent: "space-between",
                marginTop: "0.3rem",
                marginBottom: "0.6rem"
              }}
            >
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
          {sprintData.length > 0 ? (
              <select
                value={selectedOption}
                onChange={handleDropdownChange}
                style={{ paddingBlock: "0.4rem", paddingInline: "0.5rem", marginBottom: "2.5rem", borderRadius: "0.5rem", borderColor: "#f98080" }}
              >
                <option className="dropdown" value="">Select an option</option>
                {sprintData.map((item) => (
                  <option key={item.id} value={item.id} className="dropdown">
                    {item.name}
                  </option>
                ))}
              </select>
          ) : null}
        </div>
        <BarChartMaker props={engagementData}/>
      </div>
    </div>
  )
}