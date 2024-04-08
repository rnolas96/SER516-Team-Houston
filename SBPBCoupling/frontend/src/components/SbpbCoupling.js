import React from "react";
import axios from "axios";
import { useEffect, useState } from "react";
import "../App.css";
import NetworkChartMaker from "./reusable_components/NetworkChartMaker";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";

export default function SbpbCoupling() {

  const [pbCouplingData, setPbCouplingData] =
    useState({
      nodes: [
        {id: 0, label: "Waiting for data", title:  "Title Not available"},
      ],
      edges: [
          {from: 0, to: 0},
      ]
    });
  const [sbCouplingData, setSbCouplingData] =
    useState({
      nodes: [
          {id: 0, label: "Waiting for data", title:  "Title Not available"},
      ],
      edges: [
          {from: 0, to: 0},
      ]
    });

  const [projectSlug, setProjectSlug] = useState(null);

  const [isSprintDisabled, setIsSprintDisabled] = useState(true);
  const [sprintData, setSprintData] = useState([]);

  const [selectedOption, setSelectedOption] = useState("");

  const [projectId, setProjectId] = useState(null);
  const [sprintId, setSprintId] = useState(null);

  const [showLoader, setShowLoader] = useState(false);

  const [tab, setTab] = useState(0);

  const [loginState, setLoginState] = useState(false);

  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  
  function setAuthToken() {
    axios
      .post("/api/login", {
        type: "normal",
        username: userName,
        password: password,
      })
      .then((res) => {
        console.log("res", res.data);
        if (res.data[0]) {
          localStorage.setItem("authToken", res.data[2]);
          setLoginState(true);
        } else {
          alert("authentication failed");
        }
      });
  }

  const onChangeUserName = (event) => {
    setUserName(event.target.value);
  };

  const onChangePassword = (event) => {
    setPassword(event.target.value);
  };

  const clearData = () => {
    setSprintData([]);
    setSprintId(null);
    setPbCouplingData(null);
    setSbCouplingData(null);
    setSelectedOption("");
    setShowLoader(false);
    setIsSprintDisabled(true);
  };

  const handleDropdownChange = (e) => {
    setSelectedOption(e.target.value);
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
        
        if(res.data.nodes && res.data.edges) {
          updateCall(res.data);
        }

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
        if(tab == 1)
          setIsSprintDisabled(false);
        setShowLoader(true);
      });
  }

  useEffect(() => {
    const authToken = localStorage.getItem("authToken");

    if (authToken) {
      setLoginState(true);
    } else {
      setLoginState(false);
    }
  }, []);

  useEffect(() => {
    const callApis = () => {
      const authToken = localStorage.getItem("authToken");
      console.log("authToken", authToken);
      console.log("sprintId", sprintId);
      console.log("projectId", projectId);

      if (authToken && projectId) {
        apiCall(
          `/api/SbPbCoupling/pb_coupling?project_id=${projectId}`,
          setPbCouplingData,
          "Product Backlog information",
          authToken
        );
      }
      if (authToken && projectId && sprintId) {
        apiCall(
          `/api/SbPbCoupling/sb_coupling?sprint_id=${sprintId}`,
          setSbCouplingData,
          "Sprint Backlog information",
          authToken
        );
      }
    };

    callApis();
    const intervalId = setInterval(callApis, 30000);
    return () => clearInterval(intervalId);
  }, [sprintId, projectId, isSprintDisabled]);

  return (
    <div className="container-full bg-white">
      <div className="flex flex-col min-h-[100%] justify-between w-full py-[1rem] px-[2rem]">
        
      {!loginState ? (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <span className="text-[1.2rem] font-bold font-sans">Username:</span>
            <input
              className="bg-white border-2 rounded-xl hover:rounded-lg duration-300 border-[#ffd053] active:border-[#ffd053] h-[2.3rem] px-3 text-[1rem] font-sans"
              type="username"
              value={userName}
              onChange={onChangeUserName}
              aria-label="username"
              style={{ marginBottom: "20px" }}
            />
            <span className=" text-[1.2rem] font-bold font-sans">
              Password:
            </span>
            <input
              className="bg-white border-2 rounded-xl hover:rounded-lg duration-300 border-[#ffd053] active:border-[#ffd053] h-[2.3rem] px-3"
              type="password"
              value={password}
              onChange={onChangePassword}
              style={{ marginBottom: "20px" }}
            />
            <button
              className=" p-4 border-4 border-[#ffd053] hover:bg-[#ffd053] duration-300 hover:text-white font-sans font-bold rounded-2xl hover:rounded-lg"
              onClick={() => setAuthToken()}
            >
              Submit
            </button>
          </div>
        ) : (
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
          onSelect={(index)  => {
            if(index == 1) {
              setIsSprintDisabled(false)
              setTab(1);
            }
            if(index == 0) {
              setIsSprintDisabled(true);
              setTab(0);
            }
          }}
        >
          <div className="text-[2rem] w-auto rounded-none border-solid border-b-[4px] border-b-[#ffd053] font-bold bg-white hover:border-b-red-400 duration-300 font-sans text-start mt-0 pb-[0.2rem] mb-[1rem]">
            <span>SB/PB Coupling</span>
          </div>
          <TabList
            style={{ display: "flex", justifyContent: "left", border: "none" }}
          >
            <Tab
              className={"tabElements"}
              selectedClassName="selectedTabElements"
            >
              <p className="px-[0.8rem] text-center border-r-2 border-r-red-400 ">
                Product Backlog Coupling
              </p>
            </Tab>
            <Tab
              className={"tabElements"}
              selectedClassName="selectedTabElements"
              
            >
              <p className="px-[0.8rem] text-center border-none ">
                Sprint Backlog Coupling
              </p>
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
            {!isSprintDisabled && sprintData.length > 0 ? (
              <select
                value={selectedOption}
                onChange={handleDropdownChange}
                className="burndown"
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
          <TabPanel
          >
            <NetworkChartMaker
              data={pbCouplingData}
              showLoader={showLoader}
              setShowLoader={setShowLoader}
              setNodeType={"US"}
              scenario={"Enter Project Id to see the network chart"}
              
            />
          </TabPanel>
          <TabPanel 
          >
            <NetworkChartMaker
              data={sbCouplingData}
              showLoader={showLoader}
              setShowLoader={setShowLoader}
              setNodeType={"US"}
              scenario={"Enter Project Id and Sprint Id to see the network chart"}
            />
          </TabPanel>          
        </Tabs>
        )}
      </div>
    </div>
  );
}

//end of code