import './Modify.css';

import { useState, useEffect, useContext } from 'react';

import GlobalContextProvider, {GlobalContext} from '../../../contexts/GlobalContext'

function Modify() {

    const { LCLID, setProjectDataset, projectDataset, setLCLID } = useContext(GlobalContext);

    const [tableData, settableData] = useState([]);
    
    useEffect(() => {
        fetch(`http://127.0.0.1:5000/household_data_count/` + LCLID, {
            method: 'GET',
            headers: {
                'Content-Type': 'application.json',
            }
        }).then(
            res => res.json()
        ).then(
            tableData => {
                settableData(tableData.house_data_count);
            }
        )
    }, [LCLID]);

    const addLog = event => {
        event.preventDefault();
        if (LCLID !== "" && !projectDataset.includes(LCLID) ) {
            projectDataset.push(LCLID);
            setProjectDataset(projectDataset);
            setLCLID("");
        }
    }
  
    return (
        <div className="Exploration-view">
                <div className="Exploration-data-head">
                    <h2> Modify: {LCLID} </h2>
                </div>
            <div>
                <table className="Exploration-table">
                    <thead>
                        <tr>
                            <th>Column</th>
                            <th>Current value</th>
                            <th>Modified value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Start date</td>
                            <td>{tableData.min_tstp}</td>
                            <td>
                                <label>
                                    <input type="text"></input>
                                </label>
                            </td>
                        </tr>
                        <tr>
                            <td>Stop date</td>
                            <td>{tableData.max_tstp}</td>
                            <td>
                                <label>
                                    <input type="text"></input>
                                </label>
                            </td>
                        </tr>
                        <tr>
                            <td colSpan="3">
                                <button>Update Log</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <br />
                <p className="add-button" onClick={addLog}>Add <b>{LCLID}</b> to dataset</p>
            </div>

        </div>       
    );
}

export default Modify;