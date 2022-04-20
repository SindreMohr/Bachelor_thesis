import { useState, useEffect, useContext } from 'react';
import { MinimalSpinner } from 'loading-animations-react';

import './Run.css';
import ResultsPlot from './Results/ResultsPlot';

import {GlobalContext} from '../../../contexts/GlobalContext'

function Run() {

    const { ProjectID, ProjectName, modelID, setModelID, modelParam, projectDataset, Results, setResults } = useContext(GlobalContext);
    const [datasetList, setDatasetlist] = useState(<ul></ul>);
    const [runState, setRunState] = useState(false);


    function createList() {
        let content = (
            projectDataset.map(function(obj, i){
            return (
                <li key={i} >{obj}</li>
                );
            })
        );
        console.log("ok")
        return content
    }

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
        setResults(results)
        setModelID(results.mid)
        console.log(results);
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
                    <th>Prediction time [h]</th>
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

    return (
        <div className="results-wrapper">
            <div>
                <h2>Run project: <i>{ProjectName}</i></h2>
            </div>
                {runState ? <MinimalSpinner className="fidgy-spinny" color="blue" /> : content}
            
                {runState ? <button loading={runState}>Currently running</button> : <button onClick={runModel}>Run model</button>}
            <div>
            
                <table className="Exploration-table">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Value</th>
                            <th>Index</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                {Results !== "" && Results.daily_peak_dates[0]}                                
                            </td>
                            <td>
                                {Results !== "" && Results.daily_peaks[0]}
                            </td>
                            <td>
                                {Results !== "" && Results.daily_peaks_indexes[0]}
                            </td>
                        </tr>
                    </tbody>
                </table>
                {Results !== "" && <ResultsPlot />}
            </div>
        </div>       
    );
}

export default Run;