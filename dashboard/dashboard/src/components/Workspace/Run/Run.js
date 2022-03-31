import { useState, useEffect, useContext } from 'react';

import {GlobalContext} from '../../../contexts/GlobalContext'

function Run() {

    const { ProjectID, modelParam, projectDataset, LCLID } = useContext(GlobalContext);
    const [datasetList, setDatasetlist] = useState(<ul></ul>);

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

    return (
        <div className="Exploration-view">
            <div className="Exploration-data-head">
                <h2>Run {ProjectID}</h2>
            </div>
            <div className="Exploration-table-wrapper">
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
            </div>
        
            <div className="Exploration-plot-wrapper">
                <h3>Selected data:</h3>
                <ul>
                    {datasetList}
                </ul>
            </div>
            <div className="Exploration-data-head">
                
            </div>
        </div>       
    );
}

export default Run;