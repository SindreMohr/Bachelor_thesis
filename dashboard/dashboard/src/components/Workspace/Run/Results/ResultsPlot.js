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
    let ydaily_peaks = Results.daily_peaks;
    let ydaily_peaks_pred = Results.daily_peaks_predictions;
    let daily_peak_dates = Results.daily_peak_dates;

    return (
        <div>
            <h3>Predictions:</h3>
            <Plot

            data={[
        
            {

                x: xSeries.length,

                y: ySeries,
                
                

                type: 'scatter',
                name: 'energy measurements',

                mode: 'lines',

                marker: {color: 'green'},

            }, 
            {

                x: xSeries.length,

                y: Results.predictions,
                
                
                name: 'predictions',

                type: 'scatter',

                mode: 'lines',

                marker: {color: 'orange'},

            }


            ]}


            />
            <h3>Daily peak predictions:</h3>
            <Plot

            data={[

            {

                x: ydaily_peaks.length,

                y: ydaily_peaks,
                
                

                type: 'scatter',

                mode: 'lines',
                name: 'daily peaks',

                marker: {color: 'green'},

            }, 
            {

                x: ydaily_peaks.length,

                y: ydaily_peaks_pred,
                
                

                type: 'scatter',
                name: 'daily peak predictions',

                mode: 'lines',

                marker: {color: 'orange'},

            }


            ]}


            />   
            
        </div>
    );
}

export default ResultsPlot;