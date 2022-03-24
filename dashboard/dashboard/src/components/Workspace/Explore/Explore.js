import './Explore.css';
import { useState, useEffect, useContext } from 'react';

import DataPlot from '../../DataPlot/DataPlot';
import Head from './Head/Head';
import {GlobalContext} from '../../../contexts/GlobalContext'

function Explore() {

    const { LCLID } = useContext(GlobalContext);

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

    return (
        <div className="Exploration-view">
            <div className="Exploration-first-wrapper">
                <div>
                    <h2> {LCLID} </h2>
                    <table className="Exploration-table">
                        <thead>
                            <tr>
                                <th>Column</th>
                                <th>Count</th>
                                <th>Mean</th>
                                <th>Std.</th>
                                <th>Min.</th>
                                <th>Max.</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Energy</td>
                                <td>{ tableData.count_energy }</td>
                                <td>{ tableData.avg_energy }</td>
                                <td>{ tableData.std_energy }</td>
                                <td>{ tableData.min_energy }</td>
                                <td>{ tableData.max_energy }</td>
                            </tr>
                            <tr>
                                <td>Date</td>
                                <td>{ tableData.count_tstp }</td>
                                <td>{ tableData.avg_tstp }</td>
                                <td>{ tableData.std_tstp }</td>
                                <td>{ tableData.min_tstp }</td>
                                <td>{ tableData.max_tstp }</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        
            <div className="Exploration-second-wrapper">
                 <DataPlot house={LCLID} />
            </div>
            <div className="Exploration-data-head">
                <table className="Exploration-table">
                    <thead>
                        <tr>
                            <th colspan="4">Dataset head:</th>
                        </tr>
                        <tr>
                            <th>id</th>
                            <th>LCLID</th>
                            <th>tstp</th>
                            <th>Energy</th>
                        </tr>
                    </thead>
                    <Head tableData={tableData} />
                </table>
            </div>
        </div>       
    );
}

export default Explore;