import { React, useEffect, useState } from 'react';
import Loader from './Loader';
import Graph from 'react-graph-vis';
import { v4 as uuidv4 } from 'uuid';

export default function NetworkChartMaker (props) {
    console.log("propsData", props.data);

    const [updated, setUpdated] = useState(null)

    useEffect(() => {
        props.setShowLoader(false);
        if (props.data) {
            setUpdated(
                {
                nodes : props.data && props.data.nodes ? convertKeys(props.data.nodes) : [{id: 1, label: "No data"}],
                edges : [{from: 1, to: 1}]
                })
            console.log("updatedSet: ", updated);
        }
    }, [props.data, updated])

    // const [populateGraph, setPopulateGraph] = useState(null);
    
    function convertKeys(obj) {
        if (typeof obj !== "object" || obj === null) {
          return obj;
        }
        const newObj = {};
        for (const key in obj) {
          const newKey = key.replace(/"/g, "");
          newObj[newKey] = convertKeys(obj[key]); // Recursively convert nested objects
        }
        return newObj;
      }
 
        // const nodes = props.data && props.data.nodes ? convertKeys(props.data.nodes) : [{id: 1, label: "No data"}]
        // const edges = props.data && props.data.edges ? convertKeys(props.data.edges) : [{from: 1, to: 1}]

        console.log("Updated: ", updated);

    

    // const graph = {
    //     nodes: [
    //         {id: props.data ? props.data.id : 0, label: props.data ? ("US #", props.data.label) : "No label available", title: props.data ? props.data.title : "Title Not available"},
    //     ],
    //     edges: [
    //         {from: props.data ? props.data.id : 0, to: props.data ? props.data.id : 0},
    //     ]
    // }

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
    }

    return (
        <div className='graph-container'>
            {props && props.showLoader? 
          <Loader /> 
          : <div className='h-auto border-solid border-red-400 border-2 w-full rounded-xl'>
          <Graph
              graph={updated}
              options={option}
              key={uuidv4()}
          />
        </div>
        }
        </div>
    );
}