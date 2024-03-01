import React, { useEffect, useState } from 'react'
import '../App.css'
import SidebarMenu from './SidebarMenu'
import axios from 'axios'
import BarChartMaker from './reusable_components/BarChartMaker';
import { selectClasses } from '@mui/material';
import Loader from './reusable_components/Loader';
export default function Engagement() {

  const [engagementData, setEngagementData] = useState(null);
  const [barChartData, setBarChartData] = useState(null);

  const [projectSlug, setProjectSlug] = useState(null);
  const [engagementDataLabels, setEngagementDataLabels] = useState([]);

  const [selectedOption, setSelectedOption] = useState("");

  const [projectId, setProjectId] = useState(null);

  const [showLoader, setShowLoader] = useState(false);

  const clearData = () => {
    setEngagementDataLabels([]);
    setEngagementData(null);
    setShowLoader(false);
    setBarChartData(null);
  };

  const handleDropdownChange = (e) => {
    setSelectedOption(e.target.value);
    setShowLoader(true);
  };

  function onChangeProjectSlug(event) {
    setProjectSlug(event.target.value);
    clearData();
  }

  function setEngagementDetails() {
    const authToken = localStorage.getItem("authToken");
    const projectDataUrl = `/api/project/milestone_data?project_slug=${projectSlug}`;
    setShowLoader(true);
    async function fetchData() {
      try {
        const projectDataResponse = await axios.get(projectDataUrl, {
          headers: {
            Authorization: authToken,
          },
        });
    
        const projectId = Object.keys(projectDataResponse.data)[0];
        setProjectId(projectId);

        const engagementUrl = `/api/engagement/taiga_member_engagement?project_id=${projectId}`;
        const engagementDataResponse = await axios.get(engagementUrl, {
          headers: {
            Authorization: authToken,
          },
        });
        
        const metricLabels = Object.keys(engagementDataResponse.data);

        setEngagementData(engagementDataResponse.data);

        setEngagementDataLabels(metricLabels);
        setShowLoader(false);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }

    fetchData();
  }
  
  useEffect(() => {
    if (engagementData && selectedOption !== "")
      populateData(selectedOption, engagementData[selectedOption]);

    if (selectedOption === "")
      clearData();

  }, [selectedOption]);
  
  function populateData(metricLabel, engagementValue)
  {
    const updated = {
      labels: Object.keys(engagementValue),
      text: "Engagement data",
      datasets: [
        {
          label: formatString(metricLabel),
          data: engagementValue,
          backgroundColor: [
            'rgb(255, 99, 132)'
          ],
          hoverOffset: 4
        }
      ]
    }
    setBarChartData(updated);
    setShowLoader(false);
  }

  function formatString(originalString)
  {
    const formattedString = originalString.split("_").map((word) => word.charAt(0).toUpperCase() + word.slice(1)).join(" ");

    return formattedString
  }

  return (
    <div className='container-full'>
      <div className="route-container flex flex-col min-h-[100%]">
        <div
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              width: "50%",
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
              onClick={() => setEngagementDetails()}
            >
              Submit
            </button>
          </div>
          <div style = {{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          {showLoader && <Loader/>} {}
          </div>
          {engagementDataLabels.length > 0 ? (
              <select
                value={selectedOption}
                onChange={handleDropdownChange}
                style={{ paddingBlock: "0.4rem", paddingInline: "0.5rem", marginBottom: "2.5rem", borderRadius: "0.5rem", borderColor: "#f98080" }}
              >
                <option className="dropdown" value="">Select an option</option>
                {engagementDataLabels.map((item) => (
                  <option value={item} className="dropdown">
                    {formatString(item)}
                  </option>
                ))}
              </select>
          ) : null}
        </div> 
        {barChartData ? <BarChartMaker props={barChartData}/>: null}
      </div>
    </div>
  )
}