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

import { Line } from "react-chartjs-2"

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

export default function LineChartMaker({props}) {

    console.log("props", props);

    const options = {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: props.text,
        },
      },
    };
    const data = {
      labels: props.labels,
      datasets: props.datasets
    };

    return (
      <div className='graph-container'>
        <Line 
          data = {data} 
          options = {options}
        />
      </div>
    );
}