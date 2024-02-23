export default function NetworkChartMaker (props) {
    return (
        <div className='graph-container'>
            {props.data?
                <div>Network Chart displayed</div>
                : <div>{props.scenario? props.scenario : "Enter data to see chart"}</div>
            }   
        </div>
    );
}