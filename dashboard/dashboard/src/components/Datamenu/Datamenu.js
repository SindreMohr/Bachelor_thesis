import { useState, useEffect } from 'react';

import './Datamenu.css';

function Datamenu() {

    const [data, setData] = useState([]);
    const api_call = {content: 'all'}

    useEffect(() => {
        fetch(`http://127.0.0.1:5000/get_data`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application.json',
            },
            body: JSON.stringify(api_call),
        }).then(
            res => res.json()
        ).then(
            data => {
                setData(data.data);
            }
        )
    }, []);

    const listItems = data.map((d) =>  <li className="data-menu-output">{d}</li>);

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