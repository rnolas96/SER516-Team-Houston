import axios from 'axios';
import { useEffect, useState } from 'react';

export default function ChartMaker() {

    const [info, setInfo] = useState("");

    useEffect (() => {
        axios.get('/api').then(res => setInfo(res.data));
    }, []);

    console.log("info", info);

    return (
        <p>{info}</p>
    );
}