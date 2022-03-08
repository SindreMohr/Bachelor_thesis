import Plot from 'react-plotly.js';


import { useState, useEffect } from 'react';

function DataPlot() {

    const [data, setData] = useState([]);
    const api_call = {content: 'MAC234'}

    useEffect(() => {
        fetch(`http://127.0.0.1:5000/get_data`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application.json',
            },
            body: JSON.stringify(api_call),
        }).then(
            res => res.json()
        ).then(
            data => {
                setData(data.data);
            }
        )
    }, []);
    return (
        <Plot

        data={[

        {

            x: Array.from(Array(data.length).keys()),

            y: data,

            type: 'scatter',

            mode: 'lines+markers',

            marker: {color: 'red'},

        },

        {type: 'bar', x: Array.from(Array(data.length).keys()), y: data},

        ]}


        />
    );
}

export default DataPlot;