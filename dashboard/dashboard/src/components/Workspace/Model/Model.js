import './Model.css';
import { useState, useContext } from 'react';
// import Slider from 'react-rangeslider'
// import 'react-rangeslider/lib/index.css'

import {GlobalContext} from '../../../contexts/GlobalContext'

function Model() {

    //const [formOption, setFormOption] = useState("options")

    const { setModelParam } = useContext(GlobalContext);

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
                    <h2> Model </h2>
                    <table className="Exploration-table">
                        <thead>
                            <tr>
                                <th>T</th>
                                <th>A</th>
                                <th>B</th>
                                <th>L</th>
                                <th>E</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                            </tr>
                            <tr>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                            </tr>

                        </tbody>
                    </table>
                </div>
            </div>
        
            <div className="Exploration-second-wrapper grey-bg">
                {/* <div className="Model-menu">
                    <ul>
                        <li onClick={() => setForm('options')}>Model Options</li>
                        <li onClick={() => setForm('parameters')}>Model Parameters</li>
                    </ul>
                </div> */}
                { Options }
                {/* { formOption === "options" ?
                Options
                : formOption === "parameters" ?
                <h1>Parameters</h1>
    : null } */}
            </div>
        </div>       
    );
}

export default Model;