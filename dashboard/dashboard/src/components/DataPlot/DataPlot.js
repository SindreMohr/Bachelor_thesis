import Plot from 'react-plotly.js';


import { useState, useEffect } from 'react';

function DataPlot() {

    const [data, setData] = useState([]);
    const api_call = {content: 'MAC000150'}

    useEffect(() => {
        fetch(`http://127.0.0.1:5000/household_data_curve/` + api_call.content, {
            method: 'GET',
            headers: {
                'Content-Type': 'application.json',
            }
        }).then(
            res => res.json()
        ).then(
            data => {
                setData(data.house_data);
            }
        )
    }, []);
    return (
        <Plot

        data={[

        {

            x: data.time,

            y: data.values,

            type: 'bar',

            mode: 'lines+markers',

            marker: {color: 'green'},

        },


        ]}


        />
    );
}

export default DataPlot;