import React from "react";
import axios from "axios";
import { useEffect, useState } from "react";
import "../App.css";
import LineChartMaker from "./reusable_components/LineChartMaker";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";
import { Buffer } from "buffer";

export default function CostOfDelay() {

  const [storyPointData, setStoryPointData] = useState(null);
  const [businessValueData, setBusinessValueData] = useState(null);
  const [costOfDelayData, setCostOfDelayData] =
    useState(null);

  const [projectSlug, setProjectSlug] = useState(null);
  const [sprintData, setSprintData] = useState([]);

  const [selectedOption, setSelectedOption] = useState("");

  const [projectId, setProjectId] = useState(null);
  const [sprintId, setSprintId] = useState(null);

  const [businessValueCostFactorInput, setBusinessValueCostFactorInput] = useState("")
  const [businessValueCostFactor, setBusinessValueCostFactor] = useState(null);

  const [showLoader, setShowLoader] = useState(false);

  const clearData = () => {
    setSprintData([]);
    setSprintId(null);
    setStoryPointData(null);
    setBusinessValueData(null);
    setCostOfDelayData(null);
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

  function onChangeBusinessValueCostFactor(event) {
    setBusinessValueCostFactorInput(event.target.value);
    setCostOfDelayData(null);
    console.log("cost factor", businessValueCostFactor)
  }

  function createUpdatedData(labels, values, updateCall, scenario) {
    labels[0] = "";
    const updated= {
      labels: labels,
      text: scenario,
      datasets: [
        {
          label: "Actual Path",
          data: values,
          borderColor: "orange",
          backgroundColor: ["rgb(255, 99, 132)", "rgb(255, 205, 86)"],
          hoverOffset: 4,
        },
      ],
    };

    updateCall(updated);
  }

  function apiCall(url, authToken) {
    axios
      .get(url, {
        headers: {
          Authorization: authToken,
        },
      })
      .then((res) => {
        console.log("res", res.data);
    
        const data = res.data;

        const labels = Object.keys(data['userstory']);
        const storyPointValues = Object.values(data['userstory']);
        const businessValues = Object.values(data['business_value']);
        const costOfDelayValues = Object.values(data['cost_of_delay']);

        setShowLoader(false);

        createUpdatedData(labels, storyPointValues, setStoryPointData, "storypoints graph");
        createUpdatedData(labels, businessValues, setBusinessValueData, "business value graph");
        createUpdatedData(labels, costOfDelayValues, setCostOfDelayData, "cost of delay graph");

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
        console.log(s_Data);
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

      if (authToken && projectId && sprintId && businessValueCostFactor) {
        apiCall(
          `/api/task/cost_of_delay?project_id=${projectId}&sprint_id=${sprintId}&business_value_cost_factor=${businessValueCostFactor}`,
          authToken
        );
      }
    };

    callApis();
    const intervalId = setInterval(callApis, 30000);
    return () => clearInterval(intervalId);
  }, [sprintId, projectId, businessValueCostFactor]);

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
                Storypoints Affected
              </p>
            </Tab>
            <Tab
              className={"tabElements"}
              selectedClassName="selectedTabElements"
            >
              <p className="px-[0.8rem] text-center border-r-2 border-r-red-400 ">
                Business Value Affected
              </p>
            </Tab>
            <Tab
              className={"tabElements"}
              selectedClassName="selectedTabElements"
            >
              <p className="px-[0.8rem] text-center border-none ">
                Cost of Delay
              </p>
            </Tab>
          </TabList>
          <div style={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "start",
            marginTop: "0.3rem",
            marginBottom: "0.6rem",
          }}>
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                width: "30%",
                // minHeight: "50%"
              }}
              className="parent"
            >

              <span className="text-[1rem] font-bold font-sans">
                Project Slug:
              </span>
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
                className="bg-white border-2 rounded-xl hover:rounded-none duration-300 border-[#ffd053] h-[2.3rem] px-3 w-[80%] text-[1rem] font-sans"
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
            <div style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                width: "30%",
                // minHeight: "50%"
              }}
              className="parent ml-[2rem]"
            >
              <div className="flex flex-col">
              <span className="text-[1rem] font-bold font-sans">
                BV Cost Factor:
              </span>
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
                  className="bg-white border-2 rounded-xl hover:rounded-none duration-300 border-[#ffd053] h-[2.3rem] px-3 w-[80%] text-[1rem] font-sans"
                  type="number"
                  value={businessValueCostFactorInput}
                  onChange={onChangeBusinessValueCostFactor}
                  aria-label="username"
                />
                <button
                  className="ml-[0.6rem] h-[2.45rem] w-[33%] border-4 border-[#ffd053] hover:bg-[#ffd053] duration-300 hover:text-white font-sans font-bold rounded-2xl hover:rounded-none"
                  onClick={() => setBusinessValueCostFactor(businessValueCostFactorInput)}
                >
                  Submit
                </button>
              </div>
              </div>
            </div>
          </div>
          <TabPanel>
            <LineChartMaker
              data={storyPointData}
              showLoader={showLoader}
            />
          </TabPanel>
          <TabPanel>
            <LineChartMaker
              data={businessValueData}
              showLoader={showLoader}
            />
          </TabPanel> 
          <TabPanel>
            <LineChartMaker
              data={costOfDelayData}
              showLoader={showLoader}
            />
          </TabPanel> 
        </Tabs>
      </div>
    </div>
  );
}
