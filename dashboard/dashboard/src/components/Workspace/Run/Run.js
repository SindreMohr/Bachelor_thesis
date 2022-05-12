import { useState, useEffect, useContext, useRef} from 'react';

import { MinimalSpinner } from 'loading-animations-react';
import { useReactToPrint } from 'react-to-print';


import './Run.css';
import ResultsPlot from './Results/ResultsPlot';

import {GlobalContext} from '../../../contexts/GlobalContext'

function Run() {

    const { ProjectID, ProjectName, modelID, setModelID, modelParam, projectDataset, Results, setResults } = useContext(GlobalContext);
    const [datasetList, setDatasetlist] = useState(<ul></ul>);
    const [runState, setRunState] = useState(false);

    const [resultsTable, setResultsTable] = useState([]);

    function makeTable(xDates, yMeasure) {
        let content = (
            yMeasure.map(function(measure, index){
                return (
                    <tr key={index}>
                        <td>
                        {index}                                
                    </td>
                    <td>
                        {xDates[index]}                                
                    </td>
                    <td>
                        {measure}                                
                    </td>
                    <td>
                        {Results.predictions[index].toFixed(3)}
                    </td>
                </tr>
                );
            })
        );
        return content
    }
    
    useEffect(() => {
        if (Results.time) {
            const xDates = Results.time.slice(-Results.predictions.length,Results.time.length);
            const yMeasure = Results.energy_data.slice(-Results.predictions.length, Results.energy_data.length);
            console.log(xDates);
            console.log(yMeasure);
            setResultsTable([]);
        }
    }, [Results]);

    function createList() {
        let content = (
            projectDataset.map(function(obj, i){
            return (
                <li key={i} >{obj}</li>
                );
            })
        );
        return content
    }

    const printContent = useRef();
    const savePDF = useReactToPrint({
        content: () => printContent.current,
        documentTitle: ProjectName,
        copyStyles: true,
    });


    useEffect(() => {
        if (projectDataset[0]) {
            setDatasetlist(                  
                createList()
            );
        } else {
            setDatasetlist(<ul></ul>);
        };
    }, [projectDataset]);

    async function runModel() {
        let content = {}
        setRunState(true);
        content.dataset = projectDataset
        content.parameters = modelParam
        content.projectID = ProjectID
        content.mid = modelID
       
        const url = "http://localhost:5000/"
        const reqOpt = {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              content
            }),
          };
        const respons = await fetch(url + "run-model", reqOpt);
        const results = await respons.json();
        console.log(results)
        if (results != null){
            setResults(results);
            setModelID(results.mid);
        }
       
        setRunState(false);
    }

    const content = (<div>
        <h3>Settings:</h3>
        <table className="Exploration-table">
            <thead>
                <tr>
                    <th>Model</th>
                    <th>Training [%]</th>
                    <th>Test [%]</th>
                    <th>Epochs</th>
                    <th>Lag</th>
                    <th>Layer</th>
                    <th>Prediction time [hh]</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        {modelParam.model}                                
                    </td>
                    <td>
                        {modelParam.training}
                    </td>
                    <td>
                        {modelParam.training > 0 && 100 - modelParam.training}
                    </td>
                    <td>
                        {modelParam.epoch}
                    </td>
                    <td>
                        {modelParam.lag}
                    </td>
                    <td>
                        {modelParam.layer}
                    </td>
                    <td>
                        {modelParam.prediction}
                    </td>
                </tr>
            </tbody>
        </table>
        <h3>Selected data:</h3>
        <ul className='select-data-list'>
            {datasetList}
        </ul>
    </div>);


    const predictionResult = (
        <span>
            <p>
                Predicted value for {modelParam.prediction}: __ KwH
            </p>
        </span>
    )

    const printContentVar = (
        <div ref={printContent} className="pdf-wrapper">
            <h1 className="pdf-title">Project: {ProjectName}</h1>
            <div className="pdf-content">
                <h2 className="pdf-h2-title">Introduction</h2>
                <p>
                    This project utlizes an {modelParam.model.toUpperCase()} model to make predictions about energy consumption.
                    <br />
                    {modelParam.model === "lstm" ?
                    "A Long Short-Term Memory model is designed to overcome the long-term dependency problem of recurrent neural networks. LSTM may retain useful data in a sequence instead of treating each vector independently."
                    : modelParam.model === "mlp" ?
                    "A multilayer perceptron model is an artificial neural network consisting of multiple hidden layers. With only a single layer it would be a singlelayer perceptron."
                    : modelParam.model === "dt" ?
                    "A Decision tree (DT) model is a learning algorithm used for classification and regression purposes. It uses a tree structure to make decisions."
                    :null}
                </p>    
                <p>
                    The dataset is based on data from smartmeters in London. 
                    The datacolletion was done by ACORN, and the total dataset consists of 167 817 021 data entries. 
                    In this project we utilize the halfhourly dataset. Which has less attributes, but a far greater amount of data.
                </p>
                <p className='pdf-subtitle'>Wordlist:</p>
                <ul className="pdf-ul">
                    <li><b>MSE</b> - Mean Square Error</li>
                    <li><b>RMSE</b> - Root Mean Square Error</li>
                    <li><b>MAE</b> - Mean Absolute Error</li>
                    <li><b>MAPE</b> - Mean Absolute Percentage Error</li>
                </ul>
                <h2 className="pdf-h2-title">Project parameters</h2>
                <table className="Exploration-table">
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Training [%]</th>
                            <th>Test [%]</th>
                            <th>Epochs</th>
                            <th>Lag</th>
                            <th>Layer</th>
                            <th>Prediction time [hh]</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                {modelParam.model}                                
                            </td>
                            <td>
                                {modelParam.training}
                            </td>
                            <td>
                                {modelParam.training > 0 && 100 - modelParam.training}
                            </td>
                            <td>
                                {modelParam.epoch}
                            </td>
                            <td>
                                {modelParam.lag}
                            </td>
                            <td>
                                {modelParam.layer}
                            </td>
                            <td>
                                {modelParam.prediction}
                            </td>
                        </tr>
                    </tbody>
                </table>
                <h2 className="pdf-h2-title">Project dataset</h2>
                <ul className='select-data-list'>
                    {datasetList}
                </ul>
                <h2 className="pdf-h2-title">Results</h2>
                <table className="Exploration-table">
                    <thead>
                        <tr>
                            <th>MSE</th>
                            <th>RMSE</th>
                            <th>MAE</th>
                            <th>MAPE</th>
                            <th>Daily Peak MAPE</th>

                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                {Results !== "" && Results.mse.toFixed(4)}                                
                            </td>
                            <td>
                                {Results !== "" && Results.rmse.toFixed(4)}
                            </td>
                            <td>
                                {Results !== "" && Results.mae.toFixed(4)}
                            </td>
                            <td>
                                {Results !== "" && Results.mape.toFixed(2)}
                            </td>
                            <td>
                                {Results !== "" && Results.daily_peaks_res.toFixed(2)}
                            </td>
                        </tr>
                    </tbody>
                </table>
                <h2 className="pdf-h2-title">Plots</h2>
                <ResultsPlot />
            </div>
        </div>
    ); 

    return (
        <div className="results-wrapper">
            {!ProjectName 
            ?
            <span>
                <div>
                    <p>Load project to run</p>
                </div>
            </span>
            : 
            <span>
                <div>
                    <h2>Run project: <i>{ProjectName}</i></h2>
                    {runState ? <p loading={runState}>Currently running</p> : <button className="blue-btn" onClick={runModel}>Run model</button>}
                    {Results ?
                        <button className='export-button-small' onClick={savePDF}>
                            <span className="material-icons-outlined">
                                file_download
                            </span>
                            Export PDF
                        </button>: null}
                </div>
                    {runState ? <MinimalSpinner className="fidgy-spinny" color="blue" /> : content}
                
                <div>
                    {
                    Results ?

                    <table className="Exploration-table">
                        <thead>
                            <tr>
                                <th>MSE</th>
                                <th>RMSE</th>
                                <th>MAE</th>
                                <th>MAPE</th>
                                <th>Daily Peak MAPE</th>

                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>
                                    {Results !== "" && Results.mse.toFixed(4)}                                
                                </td>
                                <td>
                                    {Results !== "" && Results.rmse.toFixed(4)}
                                </td>
                                <td>
                                    {Results !== "" && Results.mae.toFixed(4)}
                                </td>
                                <td>
                                    {Results !== "" && Results.mape.toFixed(2)}
                                </td>
                                <td>
                                    {Results !== "" && Results.daily_peaks_res.toFixed(2)}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    : null    
                    }

                    {Results !== "" && <ResultsPlot />}

                    {
                    Results ?

                    <table className="Exploration-table">
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Test Value</th>
                                <th>prediction</th>
                            </tr>
                        </thead>
                        <tbody>
                            {resultsTable}
                        </tbody>
                        
                    </table>
                    : null    
                    }

                    </div>
                    {Results ? 
                        <span>
                            {printContentVar}
                        <p className="export-button-wide" onClick={savePDF}>Export PDF</p>
                        </span>
                        :
                null
            }
            </span>
            }
        </div>       
    );
}

export default Run;