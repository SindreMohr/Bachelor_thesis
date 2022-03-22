import './Workspacenav.css';

import React, { useContext } from 'react';

import {GlobalContext} from '../../../contexts/GlobalContext'

function Workspacenav() {
    const {setPAGE} = useContext(GlobalContext)
    function changeContext(value) {
        console.log(value);
        setPAGE(value);
    }
    return (
        <div className="Workspace-nav">
            <ul>
                <li onClick={() => changeContext('Explore')}>Explore</li>
                <li onClick={() => changeContext('Modify')}>Modify</li>
                <li onClick={() => changeContext('Model')}>Model Parameters</li>
                <li onClick={() => changeContext('Run')}>Run</li>
            </ul>
        </div>
    );
}

export default Workspacenav;