import './Model.css';
import { useState, useContext, useEffect } from 'react';

import {GlobalContext} from '../../../contexts/GlobalContext'

function Model() {


    const { setModelParam, modelParam } = useContext(GlobalContext);

    const [modelTypeValue, setModelTypeValue] = useState("lstm");
    const [slideValue, setSlideValue] = useState(70);
    const [epochsValue, setEpochsValue] = useState(10);
    const [lagValue, setLagValue] = useState(24);
    const [layerValue, setLayerValue] = useState(1);
    const [predictionValue, setPredictionValue] = useState(0);

    let layerDict = {};
    const [currentLayer, setCurrentLayer] = useState("1");
    const [currentLayerValue, setCurrentLayerValue] = useState("30");
    const [layerSelect, setLayerSelect] = useState([]);

    useEffect(() => {
        let result = [];
        let item;
        for (let i=1;i<=layerValue; i++) {
            item = (<option key={i} value={i}>{i}</option>);
            result.push(item);
        }
        setLayerSelect(result);
    },[layerValue]);

    const setForm = (event) => {
        event.preventDefault();

        let ModelFormData = {
            model: modelTypeValue,
            training: slideValue,
            epoch: epochsValue,
            lag: lagValue,
            layer: layerValue,
            prediction: predictionValue,
            layerDictionary: layerDict
        }
        //dt epoch 1
        if(modelTypeValue === "dt"){
            ModelFormData.epoch = "1"
        }
        console.log(ModelFormData);
        setModelParam(ModelFormData);
    }

    function handleSlideInput(e) {
        setSlideValue(e.target.value);
        console.log(slideValue)
    }

    const updateLayer = (event) =>  {
        event.preventDefault();
        layerDict[currentLayer] = currentLayerValue;
        console.log(layerDict);
    }

    const Options = (
        <form className="model-form">
            <fieldset>
                <legend><h2>Form Parameters</h2></legend>
                <label>
                    Select Model:
                    <select id="model_type" onChange={(e) => setModelTypeValue(e.target.value)}>
                        <option defaultValue="lstm" value="lstm">LSTM</option>
                        <option value="mlp">MLP</option>
                        <option value="dt">Decision Tree</option>
                    </select>
                </label>
                <label>
                    Training / Test splitt
                    <input id="splitt" type="range" value={slideValue} min="0" max="100" onChange={handleSlideInput} />
                    Training: {slideValue} %
                    Test: {100 - slideValue} %
                </label>
                { modelTypeValue !== "dt" ? 
                <label>
                    Epochs: 
                    <input id="epochs" type="number" value={epochsValue} onChange={(e) => setEpochsValue(e.target.value)}/>
                </label>
                : null}
                <label>
                    Lag: 
                    <input id="lag" type="number" value={lagValue}  onChange={(e) => setLagValue(e.target.value)}/>
                </label>
                <label>
                    Layers: 
                    <input id="layer" type="number" value={layerValue}  onChange={(e) => setLayerValue(e.target.value)}/>
                </label>
                <label>
                    Prediction time: 
                    <input id="prediction" type="number" value={predictionValue}  onChange={(e) => setPredictionValue(e.target.value)}/>
                </label>
                
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
                </div>
            </div>
        
            <div className="Exploration-second-wrapper form-bg">
                { Options }
                { modelTypeValue === "lstm" && layerValue > 0 ?
                    <form className="model-form layer-form">
                        <fieldset>
                            <legend>Layer select</legend>
                            <label>
                                <select onChange={(e) => setCurrentLayer(e.target.value)}>
                                    {layerSelect}
                                </select>
                            </label>                
                            <label>
                                Value:
                                <input type="number" value={currentLayerValue}  onChange={(e) => setCurrentLayerValue(e.target.value)}/>
                            </label>
                            <button onClick={updateLayer}>Update Layer</button>
                        </fieldset>
                    </form>
                : modelTypeValue === "mlp" && layerValue > 0 ?
                    <form className="model-form layer-form">
                        <fieldset>
                            <legend>Layer select</legend>
                            <label>
                                <select onChange={(e) => setCurrentLayer(e.target.value)}>
                                {layerSelect}
                                </select>
                            </label>                
                            <label>
                                Value:
                                <input type="number" value={currentLayerValue}  onChange={(e) => setCurrentLayerValue(e.target.value)}/>
                            </label>
                            <button onClick={updateLayer}>Update Layer</button>
                        </fieldset>
                    </form>
                : null }
                <button className="blue-btn" onClick={setForm}>Update model</button>
            </div>
        </div>       
    );
}

export default Model;