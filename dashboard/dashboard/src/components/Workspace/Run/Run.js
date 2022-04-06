import { useState, useEffect, useContext } from 'react';

import {GlobalContext, projectDataset, modelParam, projectID} from '../../../contexts/GlobalContext'

function Run() {

    const { ProjectID, modelParam, projectDataset, LCLID } = useContext(GlobalContext);
    const [datasetList, setDatasetlist] = useState(<ul></ul>);
    const [Results, setResults] = useState();

    useEffect(() => {
        if (projectDataset[0]) {
            setDatasetlist(                  
                projectDataset.map(function(obj, i){
                    return (
                        <li key={i} >{projectDataset[i]}</li>
                    );
                })
            );
        };
    }, [LCLID]);

    async function runModel() {
        let content = {}
        content.dataset = projectDataset
        content.parameters = modelParam
        content.projectID = ProjectID
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
        console.log(results);
    }

    return (
        <div>
            <div className="Exploration-data-head">
                <h2>Run {ProjectID}</h2>
            </div>
            <div>
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
                <ul>
                    {datasetList}
                </ul>
            </div>
                <button onClick={runModel}>run this thing</button>
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
                                {Results.daily_peak_dates[0]}                                
                            </td>
                            <td>
                                {Results.daily_peaks[0]}
                            </td>
                            <td>
                                {Results.daily_peaks_indexes[0]}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>       
    );
}

export default Run;