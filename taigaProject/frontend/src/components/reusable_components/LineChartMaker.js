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

import Loader from './Loader';

import '../../App.css'

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

export default function LineChartMaker(props) {

    console.log("props", props);

    const options = {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: props && props.data? props.data.text: "",
        },
      },
      indexAxis: 'x',
      scales: {
        y: {
          beginAtZero: true
        }
      }
    };
    const data = {
      labels: props && props.data? props.data.labels: [],
      datasets: props && props.data? props.data.datasets : []
    };

    return (
      <div className='w-[70%]'>
        {props && props.showLoader? 
          <Loader/> 
          : <Line 
            data = {data} 
            options = {options}
          /> 
        }
      </div>
    );
}