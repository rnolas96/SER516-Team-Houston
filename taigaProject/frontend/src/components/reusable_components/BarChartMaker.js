import { useEffect, useState } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';

import 'chart.js/auto';

import { Bar } from "react-chartjs-2"

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

export default function BarChartMaker({props}) {

    console.log("props", props);

    const options = {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: props? props.text: "",
        },
      },
    };
    const data = {
      labels: props? props.labels: [],
      datasets: props? props.datasets: []
    };

    return (
      <div className='graph-container'>
        <Bar 
          data = {data} 
          options = {options}
        />
      </div>
    );
}