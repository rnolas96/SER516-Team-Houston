import { useEffect } from 'react';
import Loader from './Loader';

export default function NetworkChartMaker (props) {

    useEffect(() => {
        if(props.data)
            props.setShowLoader(false);
    }, [props.data])

    return (
        <div className='graph-container'>
            {props.data?
                <div>Network Chart displayed</div>
                : props.showLoader? <Loader/>
                    : <div>{props.scenario? props.scenario : "Enter data to see chart"}</div>
            }   
        </div>
    );
}