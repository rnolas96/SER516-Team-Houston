import React, { useEffect, useState, useRef } from "react";
import "../App.css";
import axios from "axios";
// import { Box } from '@ant-design/plots';
import BoxPlotChartMaker from "./reusable_components/BoxPlotChartMaker";
import { DateRangePicker } from "react-date-range";
import "react-date-range/dist/styles.css";
import "react-date-range/dist/theme/default.css";
import format from 'date-fns/format'
import { addDays } from 'date-fns'

export default function CycleTime() {
  const [projectSlug, setProjectSlug] = useState(null);
  const [projectId, setProjectId] = useState(null);
  const [cycleTimeData, setCycleTimeData] = useState({});
  const [range, setRange] = useState([
    {
      startDate: new Date(),
      endDate: addDays(new Date(), 7),
      key: "selection",
    },
  ]);
  const [open, setOpen] = useState(false);
  const refOne = useRef(null);

  // const maxDate = new Date();
  // console.log(maxDate);
  const [rangedCycleTimeData, setRangedCycleTimeData] = useState({});
  const [startDate, setStartDate] = useState(new Date(2024, 1, 24)); // dummy values for testing @rkhatta
  const [endDate, setEndDate] = useState(new Date(2024, 2, 24)); // dummy values for testing @rkhatta


  function onChangeProjectSlug(event) {
    setProjectSlug(event.target.value);
  }

  function apiCall(url, updateCall, authToken) {
    axios
      .get(url, {
        headers: {
          Authorization: authToken,
        },
      })
      .then((res) => {
        console.log("data", res.data);

        let data = res.data;

        // let sprintData = [
        //   { x: 'Sprint1', y : [1, 9, 16, 22, 24]},
        //   { x: 'Sprint2', y : [2, 8, 12, 21, 28]},
        //   { x: 'Sprint3', y : [1, 7, 10, 17, 22]}
        // ]

        const cycleTimeValuesByKey = {};

        for (const key in data) {
          cycleTimeValuesByKey[key] = data[key].map(
            (item) => item["cycle_time"]
          );
        }

        let labels = Object.keys(cycleTimeValuesByKey);
        let values = Object.values(cycleTimeValuesByKey);

        let updated = {
          labels: labels,
          values: values,
        };

        updated["label"] = "Boxplot";

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
        // let p_id = 1521718
        setProjectId(p_id);
      });
  }

  useEffect(() => {
    const authToken = localStorage.getItem("authToken");
    console.log("authToken", authToken);
    if (!cycleTimeData.length && authToken && projectId) {
      apiCall(
        `/api/task/cycle_time?project_id=${projectId}`,
        setCycleTimeData,
        authToken
      );
    }
  }, [projectId]);

  useEffect(() => {
    document.addEventListener("keydown", hideOnEscape, true);
    document.addEventListener("click", hideOnClickOutside, true);
  }, []);

  const hideOnEscape = (e) => {
    console.log(e.key);
    if (e.key === "Escape") {
      setOpen(false);
    }
  };

  const hideOnClickOutside = (e) => {
    console.log(refOne.current);
    console.log(e.target);
    if (refOne.current && !refOne.current.contains(e.target)) {
      setOpen(false);
    }
  };
  
  useEffect(() => {
    const authToken = localStorage.getItem("authToken"); 

    if(projectId && startDate && endDate && authToken) {
      let formattedStartDate = startDate.toISOString().slice(0, 10);
      console.log("startdate", startDate, "    formattedStartDate", formattedStartDate);
      let formattedEndDate = endDate.toISOString().slice(0, 10);
      apiCall(`/api/task/cycle_time_time_range?project_id=${projectId}&start_date=${formattedStartDate}&end_date=${formattedEndDate}`, setRangedCycleTimeData, authToken);
    }

  }, [projectId, startDate, endDate]);
  
  return (
    <div className="container-full">
      <div
        className="flex flex-col min-h-[100%] justify-between w-[100%] pt-[1rem] pb-[1rem] px-[2rem]"
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
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
          <div className="text-[2rem] w-auto rounded-none border-solid border-b-[4px] border-b-[#ffd053] font-bold bg-white hover:border-b-red-400 duration-300 font-sans text-start mt-0 pb-[0.2rem] mb-[1rem]">
            <span>Cycle Time</span>
          </div>
          <div className="flex flex-row space-x-[1rem] w-full justify-between">
            <div className="flex flex-col space-y-[0.2rem] w-[33%]">
              <span className="text-[1rem] font-bold font-sans">
                Project Slug:
              </span>
              <input
                className="bg-white border-2 rounded-xl hover:rounded-none duration-300 border-[#ffd053] h-[2.3rem] px-3 w-full text-[1rem] font-sans"
                type="username"
                value={projectSlug}
                onChange={onChangeProjectSlug}
                aria-label="username"
              />
            </div>
            <div className="flex space-y-[0.2rem] flex-col w-[67%]">
              <span className="text-[1rem] font-bold font-sans">
                Date Range:
              </span>
              <div className="flex flex-row space-x-[0.5rem] justify-between relative">
                <input
                  value={`${format(
                    range[0].startDate,
                    "MM/dd/yyyy"
                  )} to ${format(range[0].endDate, "MM/dd/yyyy")}`}
                  readOnly
                  className="border-2 rounded-xl hover:rounded-none duration-300 border-[#ffd053] h-[2.3rem] px-3 w-[67%] text-[1rem] font-sans"
                  onClick={() => setOpen((open) => !open)}
                />

                <div ref={refOne}>
                  {open && (
                    <DateRangePicker
                      onChange={(item) => setRange([item.selection])}
                      editableDateInputs={true}
                      moveRangeOnFirstSelection={false}
                      ranges={range}
                      months={2}
                      direction="horizontal"
                      className="calendarElement font-sans"
                    />
                  )}
                </div>
                <button
                  className="h-[2.3rem] w-[50%] border-4 border-[#ffd053] hover:bg-[#ffd053] duration-300 hover:text-white font-sans font-bold rounded-xl hover:rounded-none"
                  onClick={() => setProjectDetails()}
                >
                  Submit
                </button>
              </div>
            </div>
          </div>
        </div>{" "}
        <div>
          {rangedCycleTimeData &&
            <BoxPlotChartMaker {...rangedCycleTimeData} />}
        </div>
      </div>
    </div>
  );
}