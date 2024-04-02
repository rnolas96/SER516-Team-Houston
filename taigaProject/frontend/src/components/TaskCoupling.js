import React from "react";
import axios from "axios";
import { useEffect, useState } from "react";
import "../App.css";
import NetworkChartMaker from "./reusable_components/NetworkChartMaker";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";
import { Buffer } from "buffer";

export default function TaskCoupling() {


  const [taskCouplingData, setTaskCouplingData] =
    useState(null);

  const [projectSlug, setProjectSlug] = useState(null);


  const [projectId, setProjectId] = useState(null);

  const [showLoader, setShowLoader] = useState(false);

  const [tab, setTab] = useState(0);

  const clearData = () => {
    setTaskCouplingData(null);
    setShowLoader(false);
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
        // const labels = Object.keys(res.data);
        // const values = Object.values(res.data);
        
        // labels[0] = "";
        // const updated = {
        //   labels: labels,
        //   text: "Burndown data for " + scenario,
        //   datasets: [
        //     {
        //       label: "Burndown Data",
        //       data: values,
        //       borderColor: "black",
        //       backgroundColor: ["rgb(255, 99, 132)", "rgb(255, 205, 86)"],
        //       hoverOffset: 4,
        //     },
        //   ],
        // };
        
        const updated = res.data;
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
        // let s_Data = result.data[p_id];
        setProjectId(p_id);
        setShowLoader(true);
      });
  }

  useEffect(() => {
    const callApis = () => {
      const authToken = localStorage.getItem("authToken");
      console.log("authToken", authToken);
      console.log("projectId", projectId);

      if (authToken && projectId) {
        apiCall(
          `/api/task/task_coupling?project_id=${projectId}`,
          setTaskCouplingData,
          "Task Coupling",
          authToken
        );
      }
    };

    callApis();
    const intervalId = setInterval(callApis, 30000);
    return () => clearInterval(intervalId);
  }, [projectId]);

  return (
    <div className="container-full bg-white">
      <div className="route-container flex flex-col min-h-[100%]">
        <div
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
          </div>
          <NetworkChartMaker
            data={taskCouplingData}
            showLoader={showLoader}
            setShowLoader={setShowLoader}
            setNodeType={"Task"}
            scenario={"Enter Project Id to see the network chart"}
          />
        </div>
      </div>
    </div>
  );
}