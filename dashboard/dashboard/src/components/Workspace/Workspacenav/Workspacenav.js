import './Workspacenav.css';

import React, { useContext } from 'react';

import {GlobalContext} from '../../../contexts/GlobalContext'

function Workspacenav() {
    const {setPAGE, PAGE} = useContext(GlobalContext)
    function changeContext(value) {
        setPAGE(value);
    }
    return (
        <div className="Workspace-nav">
            <ul>
                { PAGE === "Explore" ? 
                    <li className='Workspace-nav-selected'>Explore</li>
                : 
                    <li className='Workspace-nav-not-selected' onClick={() => changeContext('Explore')}>Explore</li>
                }
                { PAGE === "Model" ? 
                    <li className='Workspace-nav-selected'>Model Parameters</li>
                : 
                    <li className='Workspace-nav-not-selected' onClick={() => changeContext('Model')}>Model Parameters</li>
                }
                { PAGE === "Run" ? 
                    <li className='Workspace-nav-selected'>Run</li>
                : 
                    <li className='Workspace-nav-not-selected' onClick={() => changeContext('Run')}>Run</li>
                }
                
                
            </ul>
        </div>
    );
}

export default Workspacenav;