import Plot from 'react-plotly.js';

import {GlobalContext} from '../../contexts/GlobalContext'


import { useState, useEffect, useContext } from 'react';

function BoxPlot({house}) {

    const [data, setData] = useState([]);

    console.log(house)
    useEffect(() => {
        fetch(`http://127.0.0.1:5000/household_data_curve/` + house, {
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
    }, [house]);
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

export default BoxPlot;