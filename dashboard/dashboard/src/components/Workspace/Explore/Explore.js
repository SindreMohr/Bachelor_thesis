import './Explore.css';
import { useState, useEffect, useContext } from 'react';

import DataPlot from '../../DataPlot/DataPlot';
import GlobalContextProvider, {GlobalContext} from '../../../contexts/GlobalContext'

function Explore() {

    const { LCLID } = useContext(GlobalContext);

    const [data, setData] = useState([]);

    

    useEffect(() => {
        fetch(`http://127.0.0.1:5000/household_data_count/` + LCLID, {
            method: 'GET',
            headers: {
                'Content-Type': 'application.json',
            }
        }).then(
            res => res.json()
        ).then(
            data => {
                setData(data.house_data_count);
            }
        )
    }, [LCLID]);

  
    return (
        <div className="Exploration-view">
            <div className="Exploration-table-wrapper">
                <div className="">
                    <h2> {LCLID} </h2>
                    <table className="Exploration-table">
                        <thead>
                            <td>Column</td>
                            <td>Count</td>
                            <td>Mean</td>
                            <td>Std.</td>
                            <td>Min.</td>
                            <td>Max.</td>
                        </thead>

                        <tr>
                            <td>Energy</td>
                            <td>{ data.count_energy }</td>
                            <td>{ data.avg_energy }</td>
                            <td>{ data.std_energy }</td>
                            <td>{ data.min_energy }</td>
                            <td>{ data.max_energy }</td>
                        </tr>
                        <tr>
                            <td>Date</td>
                            <td>{ data.count_tstp }</td>
                            <td>{ data.avg_tstp }</td>
                            <td>{ data.std_tstp }</td>
                            <td>{ data.min_tstp }</td>
                            <td>{ data.max_tstp }</td>
                        </tr>
                    </table>
                </div>
            </div>
        
            <div className="Exploration-plot-wrapper">
                 <DataPlot house={LCLID} />
            </div>
            <div className="Exploration-data-head">
                head
            </div>
        </div>       
    );
}

export default Explore;