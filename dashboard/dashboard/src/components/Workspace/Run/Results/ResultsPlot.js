import Plot from 'react-plotly.js';

import { useContext } from 'react';
import {GlobalContext} from '../../../../contexts/GlobalContext'



function ResultsPlot() {

    const { Results } = useContext(GlobalContext);
    let xSeries = Results.time.slice(-Results.predictions.length,Results.time.length);
    let ySeries = Results.energy_data.slice(-Results.predictions.length, Results.energy_data.length);
    //console.log(Results.predictions.length)
    //console.log(Results.energy_data.length)
    //console.log(xSeries)
    //console.log(ySeries)
    return (
        <Plot

        data={[
      
        {

            x: xSeries.length,

            y: ySeries,
            
            

            type: 'scatter',

            mode: 'lines',

            marker: {color: 'green'},

        }, 
        {

            x: xSeries.length,

            y: Results.predictions,
            
            

            type: 'scatter',

            mode: 'lines',

            marker: {color: 'orange'},

        }


        ]}


        />   
    );
}

export default ResultsPlot;