import { useState, useEffect } from 'react';
import DatamenuItem from './DatamenuItem/DatamenuItem';


import './Datamenu.css';

function Datamenu() {

    const [data, setData] = useState([]);

    useEffect(() => {
        fetch(`http://127.0.0.1:5000/get_lclids`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application.json',
            },
        }).then(
            res => res.json()
        ).then(
            data => {
                setData(data.data.lclid);
            }
        )
    }, []);

    const listItems = data.map((d) =>  <DatamenuItem key={d} data={d} />);

    return (
        <div className="Datamenu">
            <p className="Datamenu-header">Data</p>
            <ul>
                { listItems }
            </ul>
        </div>
    );
}

export default Datamenu;