import React from "react";
import axios from "axios";
import { useEffect, useState } from "react";
import "../App.css";
import NetworkChartMaker from "./reusable_components/NetworkChartMaker";

export default function TaskCoupling() {
  const [taskCouplingData, setTaskCouplingData] = useState(null);

  const [projectSlug, setProjectSlug] = useState(null);

  const [projectId, setProjectId] = useState(null);

  const [showLoader, setShowLoader] = useState(false);

  const [loginState, setLoginState] = useState(false);
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");

  // Handling the Auth:
  const onChangeUserName = (event) => {
    setUserName(event.target.value);
  };

  const onChangePassword = (event) => {
    setPassword(event.target.value);
  };

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
      console.log("projectId", projectId);

      if (authToken && projectId) {
        apiCall(
          `/api/taskCoupling/task_coupling?project_id=${projectId}`,
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
          <div className="text-[2rem] w-auto rounded-none border-solid border-b-[4px] border-b-[#ffd053] font-bold bg-white hover:border-b-red-400 duration-300 font-sans text-start mt-0 pb-[0.2rem] mb-[1rem]">
            <span>Task Coupling</span>
          </div>
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
          </div>
          <NetworkChartMaker
            data={taskCouplingData}
            showLoader={showLoader}
            setShowLoader={setShowLoader}
            setNodeType={"Task"}
            scenario={"Enter Project Id to see the network chart"}
          />
        </div>
        )} 
      </div>
    </div>
  );
}
