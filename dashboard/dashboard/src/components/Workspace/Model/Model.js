import './Model.css';
import { useState, useContext } from 'react';
// import Slider from 'react-rangeslider'
// import 'react-rangeslider/lib/index.css'

import {GlobalContext} from '../../../contexts/GlobalContext'

function Model() {

    //const [formOption, setFormOption] = useState("options")

    const { setModelParam } = useContext(GlobalContext);
    const [slideValue, setSlideValue] = useState(70);

    function setForm(e) {
        //console.log(formOption)
        //setFormOption(e)
        //console.log(formOption)
        let ModelFormData = {model: "lstm"}
        setModelParam(ModelFormData)
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
                    <select id="model_type">
                        <option defaultValue="lstm">LSTM</option>
                        <option value="mlp">MLP</option>
                        <option value="slp">SLP</option>
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
                    <input id="epochs" type="textbox" defaultValue="10"/>
                </label>
                <label>
                    Lag: 
                    <input id="lag" type="textbox" defaultValue="0"/>
                </label>
                <label>
                    Prediction time: 
                    <input id="prediction" type="textbox" defaultValue="0"/>
                </label>
                <button type="submit">Update model</button>
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