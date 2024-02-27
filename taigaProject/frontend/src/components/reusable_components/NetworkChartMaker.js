import { React, useEffect, useState } from 'react';
import Loader from './Loader';
import Graph from 'react-graph-vis';
import { v4 as uuidv4 } from 'uuid';

export default function NetworkChartMaker (props) {

    useEffect(() => {
        if(props.data)
            props.setShowLoader(false);
    }, [props.data])

    console.log("propsData", props.data);   

    const graph = {
        nodes: [
            {id: 1, label: "Node 1", title: "Node 1 tooltip text"},
            {id: 2, label: "Node 2", title: "Node 2 tooltip text"},
            {id: 3, label: "Node 3", title: "Node 3 tooltip text"},
            {id: 4, label: "Node 4", title: "Node 4 tooltip text"}
        ],
        edges: [
            {from: 1, to: 1, smooth: {type: "curvedCW"}, arrows: {from: {enabled: true, type: "circle"}, to: {enabled: true, type: "circle"}}},
            {from: 1, to: 4},
            {from: 3, to: 1},
            {from: 3, to: 4}
        ]
    }

    const option = {
        height: "450px",
        edges: {
            color: "red"
        },
        nodes: {
            borderWidth: 2,
            size: 40,
            color: {
                border: "#000000",
            }
        },
        shadow: true,
        smooth: true
    }

    return (
        <div className='graph-container'>
            {props.data?
                <div className='h-auto border-solid border-red-400 border-2 w-full rounded-xl'>
                    <Graph 
                        graph={graph}
                        options={option}
                        key={uuidv4()}
                    />
                </div>
                : props.showLoader? <Loader/>
                    : <div>{props.scenario? props.scenario : "Enter data to see chart"}</div>
            }   
        </div>
    );
}