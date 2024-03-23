import React from "react";
import axios from "axios";
import { useEffect, useState } from "react";
import "../App.css";
import LineChartMaker from "./reusable_components/LineChartMaker";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";
import { Buffer } from "buffer";
import { Line } from "react-chartjs-2";

export default function Burndown() {
  const [businessValueBurnDownData, setBusinessValueBurnDownData] =
    useState(null);
  const [businessValueAllSprintData, setBusinessValueAllSprintData] =
    useState(null);
  const [partialStoryPointBurnDownData, setPartialStoryPointBurnDownData] =
    useState(null);
  const [fullStoryPointBurnDownData, setFullStoryPointBurnDownData] =
    useState(null);
  const [fullStoryPointAllSprintData, setFullStoryPointAllSprintData] =
    useState(null);
  const [partialStoryPointAllSprintData, setPartialStoryPointAllSprintData] = useState(null);

  const [projectSlug, setProjectSlug] = useState(null);
  const [sprintData, setSprintData] = useState([]);

  const [selectedOption, setSelectedOption] = useState("");

  const [projectId, setProjectId] = useState(null);
  const [sprintId, setSprintId] = useState(null);

  const [showLoader, setShowLoader] = useState(false);

  const clearData = () => {
    setSprintData([]);
    setSprintId(null);
    setBusinessValueBurnDownData(null);
    setBusinessValueAllSprintData(null);
    setPartialStoryPointBurnDownData(null);
    setFullStoryPointBurnDownData(null);
    setFullStoryPointAllSprintData(null);
    setPartialStoryPointAllSprintData(null);
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

  function apiCall(url, updateCall, scenario, authToken) {
    axios
      .get(url, {
        headers: {
          Authorization: authToken,
        },
      })
      .then((res) => {
        console.log("res", res.data);
        const labels = Object.keys(res.data);
        const values = Object.values(res.data);
        setShowLoader(false);

        labels[0] = "";
        const updated = {
          labels: labels,
          text: "Burndown data for " + scenario,
          datasets: [
            {
              label: "Burndown Data",
              data: values,
              borderColor: "black",
              backgroundColor: ["rgb(255, 99, 132)", "rgb(255, 205, 86)"],
              hoverOffset: 4,
            },
          ],
        };
        updateCall(updated);
      });
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
        console.log("Sprint Data: ", s_Data);
        setProjectId(p_id);
        setSprintData(s_Data);
        setShowLoader(true);
      });
  }

  useEffect(() => {
    const callApis = () => {
      const authToken = localStorage.getItem("authToken");
      console.log("authToken", authToken);
      console.log("sprintId", sprintId);
      console.log("projectId", projectId);

      if (authToken && projectId && sprintId) {
        apiCall(
          `/api/userstory/business_value_burndown?project_id=${projectId}&sprint_id=${sprintId}`,
          setBusinessValueBurnDownData,
          "business value",
          authToken
        );
      }
      if (authToken && projectId) {
        apiCall(
          `/api/userstory/business_value_burndown_for_all_sprints?project_id=${projectId}`,
          setBusinessValueAllSprintData,
          "business value for all sprints",
          authToken
        );
      }
      if (authToken && sprintId) {
        apiCall(
          `/api/userstory/partial_userstory_burndown?sprint_id=${sprintId}`,
          setPartialStoryPointBurnDownData,
          "partial storypoints",
          authToken
        );
      }
      if (authToken && sprintId) {
        apiCall(
          `/api/userstory/userstory_burndown?sprint_id=${sprintId}`,
          setFullStoryPointBurnDownData,
          "full storypoints",
          authToken
        );
      }
      if (authToken && projectId) {
        apiCall(
          `/api/userstory/userstory_burndown_for_all_sprints?project_id=${projectId}`,
          setFullStoryPointAllSprintData,
          "full storypoints for all sprints",
          authToken
        );
      }
      if (authToken && projectId)
      {
        apiCall(
          `/api/userstory/partial_story_points?project_id=${projectId}`,
          setPartialStoryPointAllSprintData,
          "Partial Storypoints for all sprints",
          authToken
        );
      }
    };

    callApis();
    const intervalId = setInterval(callApis, 30000);
    return () => clearInterval(intervalId);
  }, [sprintId, projectId]);

  return (
    <div className="container-full bg-white">
      <div className="flex flex-col min-h-[100%] justify-between w-full py-[1rem] px-[2rem]">
        <Tabs
          style={{
            fontFamily: "Poppins",
            fontWeight: "500",
            fontSize: "0.9rem",
            border: "none",
            minHeight: "75%",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <TabList
            style={{ display: "flex", justifyContent: "left", border: "none" }}
          >
            <Tab
              className={"tabElements"}
              selectedClassName="selectedTabElements"
            >
              <p className="px-[0.8rem] text-center border-r-2 border-r-red-400 ">
                Partial Story Points
              </p>
            </Tab>
            <Tab
              className={"tabElements"}
              selectedClassName="selectedTabElements"
            >
              <p className="px-[0.8rem] text-center border-r-2 border-r-red-400 ">
                Full Story Points
              </p>
            </Tab>
            <Tab
              className={"tabElements"}
              selectedClassName="selectedTabElements"
            >
              <p className="px-[0.8rem] text-center border-r-2 border-r-red-400 ">
                Full Story Points for all sprints
              </p>
            </Tab>
            <Tab
              className={"tabElements"}
              selectedClassName="selectedTabElements"
            >
              <p className="px-[0.8rem] text-center border-r-2 border-r-red-400 ">
                Business Value
              </p>
            </Tab>
            <Tab
              className={"tabElements"}
              selectedClassName="selectedTabElements"
            >
              <p className="px-[0.8rem] text-center border-r-2 border-r-red-400 ">
                Partial Story Points for all Sprints
              </p>
            </Tab>
            <Tab
              className={"tabElements"}
              selectedClassName="selectedTabElements"
            >
              <p className="px-[0.8rem] text-center">Business Value for all sprints</p>
            </Tab>
          </TabList>
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
                marginBottom: "0.6rem",
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
                className="burndown"
                style={{
                  paddingBlock: "0.4rem",
                  paddingInline: "0.5rem",
                  marginBottom: "2.5rem",
                  borderRadius: "0.5rem",
                  borderColor: "#f98080",
                }}
              >
                <option className="dropdown" value="">
                  Select an option
                </option>
                {/* <option className="dropdown" key={item.id} value={item.id}>
                  All Sprints
                </option> */}
                {/* <option className="dropdown" key={item.id} value={item.id}>
                  All Sprints
                </option> */}
                {sprintData.map((item) => (
                  <option key={item.id} value={item.id} className="dropdown">
                    {item.name}
                  </option>
                ))}
              </select>
            ) : null}
          </div>
          <TabPanel>
            <LineChartMaker
              data={partialStoryPointBurnDownData}
              showLoader={showLoader}
            />
          </TabPanel>
          <TabPanel>
            <LineChartMaker
              data={fullStoryPointBurnDownData}
              showLoader={showLoader}
            />
          </TabPanel>
          <TabPanel>
          <LineChartMaker
              data={fullStoryPointAllSprintData}
              showLoader={showLoader}
            />
          </TabPanel>
          <TabPanel>
            <LineChartMaker
              data={businessValueBurnDownData}
              showLoader={showLoader}
            />
          </TabPanel>
          <TabPanel>
            <LineChartMaker
              data={businessValueAllSprintData}
              showLoader={showLoader}
            />
          </TabPanel>
          <TabPanel>
            <LineChartMaker
              data = {partialStoryPointAllSprintData}
              showLoader = {showLoader}
              />
          </TabPanel>
        </Tabs>
      </div>
    </div>
  );
}

//end of code
