import './Model.css';
import { useState } from 'react';

function Model() {

    const [FormOption, setFormOption] = useState("options")

    function setForm(e) {
        console.log(FormOption)
        setFormOption(e)
        console.log(FormOption)
    }

    const Options = (
        <form>
            <label>
                Model select:
                <select>
                    <option selected value="">LSTM</option>
                    <option value="">LSTM</option>
                    <option value="">LSTM</option>
                    <option value="">LSTM</option>
                </select>
            </label>
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
                <div className="Model-menu">
                    <ul>
                        <li onClick={() => setForm('options')}>Model Options</li>
                        <li onClick={() => setForm('parameters')}>Model Parameters</li>
                    </ul>
                </div>
                { FormOption === "options" ?
                Options
                : FormOption === "parameters" ?
                <h1>Parameters</h1>
                : null }
            </div>
        </div>       
    );
}

export default Model;