import Plot from 'react-plotly.js';

import { useState, useEffect } from 'react';

function DataPlot({house}) {

    const [data, setData] = useState([]);

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

        <div>
            <h3>Data overview</h3>
            <Plot

            style={{width: "100%"}}

            data={[

            {

                x: data.time,

                y: data.values,

                type: 'scatter',

                mode: 'lines',

                marker: {color: ['lightblue']},

            },


            ]}


            />
            <h3>Box Plot</h3>
            <Plot

            style={{width: "100%"}}

            data={[

            {

                x: data.values,
                
            
                type: 'box',

                boxpoints: 'Outliers',
                //boxmean: 'sd',
                name: 'Energy measurements',

                marker: {color: ['lightblue']},

            },


            ]}


            />
        </div>
        
    );
}

export default DataPlot;