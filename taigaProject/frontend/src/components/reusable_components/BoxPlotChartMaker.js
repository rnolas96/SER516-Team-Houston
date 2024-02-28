import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import { BoxPlotController, BoxAndWiskers } from '@sgratzl/chartjs-chart-boxplot';

Chart.register(BoxPlotController, BoxAndWiskers);

const BoxPlotChartMaker = (props) => {
  // console.log(props, props);
  const [detail, setDetail] = useState(props);
  const chartContainer = useRef(null);

  const labels = props? props.labels : [];
  const values = props? props.values : [];

  const chartConfig = {
    type: 'boxplot',
    data: {
      labels: labels,
      datasets: [
        {
          label: props? props.label : "",
          backgroundColor: 'rgba(38,139,238,0.5)',
          borderColor: 'rgba(38,139,238)',
          borderWidth: 1,
          outlierColor: '#ffffff',
          padding: 20,
          itemRadius: 0,
          data: values
        }
      ]
    },
    tooltips: {
      mode: 'index',
      intersect: false
    },
    options: {
      
      indexAxis: 'y',
      responsive: true,
      plugins: {
        legend: {
          display: false,
          position: 'top'
        },
        title: {
          display: false
        }
      },
      scales: {
        x: {
          categoryPercentage: 0.5,
          barPercentage: 0.7
        }
      }
    }
  };

  useEffect(() => {
    const newChartInstance = new Chart(chartContainer.current, chartConfig);
    return () => {
      newChartInstance.destroy();
    };
  }, [chartContainer, detail]);

  useEffect(() => {
    setDetail(props);
  }, [props])

  return (
    <div style={{minWidth: 500, minHeight: 500}}>
      <canvas ref={chartContainer} width="100" height="100" />
    </div>
  );
};

export default BoxPlotChartMaker;