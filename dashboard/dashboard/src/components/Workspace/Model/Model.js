import './Model.css';
import { useState, useContext } from 'react';

import {GlobalContext} from '../../../contexts/GlobalContext'

function Model() {


    const { setModelParam, modelParam } = useContext(GlobalContext);

    const [modelTypeValue, setModelTypeValue] = useState("lstm");
    const [slideValue, setSlideValue] = useState(70);
    const [epochsValue, setEpochsValue] = useState(10);
    const [lagValue, setLagValue] = useState(24);
    const [layerValue, setLayerValue] = useState(1);
    const [predictionValue, setPredictionValue] = useState(0);

    const setForm = (event) => {
        event.preventDefault();

        let ModelFormData = {
            model: modelTypeValue,
            training: slideValue,
            epoch: epochsValue,
            lag: lagValue,
            layer: lagValue,
            prediction: predictionValue
        }
        console.log(ModelFormData);
        setModelParam(ModelFormData);
    }

    function handleSlideInput(e) {
        setSlideValue(e.target.value);
        console.log(slideValue)
    }

    const Options = (
        <form className="model-form">
            <fieldset>
                <legend>Form Parameters</legend>
                <label>
                    Select Model:
                    <select id="model_type" onChange={(e) => setModelTypeValue(e.target.value)}>
                        <option defaultValue="lstm">LSTM</option>
                        <option value="mlp">MLP</option>
                        <option value="slp">SLP</option>
                        <option value="dt">Decision Tree</option>
                    </select>
                </label>
                <label>
                    Training / Test splitt
                    <input id="splitt" type="range" value={slideValue} min="0" max="100" onChange={handleSlideInput} />
                    Training: {slideValue} %
                    Test: {100 - slideValue} %
                </label>
                <label>
                    Epochs: 
                    <input id="epochs" type="number" value={epochsValue} onChange={(e) => setEpochsValue(e.target.value)}/>
                </label>
                <label>
                    Lag: 
                    <input id="lag" type="number" value={lagValue}  onChange={(e) => setLagValue(e.target.value)}/>
                </label>
                <label>
                    Layer: 
                    <input id="layer" type="number" value={layerValue}  onChange={(e) => setLayerValue(e.target.value)}/>
                </label>
                <label>
                    Prediction time: 
                    <input id="prediction" type="number" value={predictionValue}  onChange={(e) => setPredictionValue(e.target.value)}/>
                </label>
                <button onClick={setForm}>Update model</button>
            </fieldset>
        </form>
    );
  
    return (
        <div className="Exploration-view">
            <div className="Exploration-first-wrapper">
                <div className="">
                    <h2> Current Parameters </h2>
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
            </div>
        
            <div className="Exploration-second-wrapper grey-bg">
                { Options }
            </div>
        </div>       
    );
}

export default Model;