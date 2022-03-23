import './Workspace.css';
import Workspacenav from './Workspacenav/Workspacenav';
import Explore from './Explore/Explore';
import Modify from './Modify/Modify';
import Model from './Model/Model';
import Run from './Run/Run';

import { useContext } from 'react';
import {GlobalContext} from '../../contexts/GlobalContext'

function Workspace() {
    const {PAGE} = useContext(GlobalContext)
    return (
        <div className="Workspace">
           <div className="Workspace-content">
                <Workspacenav />
                { PAGE === "Explore" ?
                <Explore />
                : PAGE === "Modify" ?
                <Modify />
                : PAGE === "Model" ?
                <Model />
                : PAGE === "Run" ?
                <Run />
                : null }
           </div>
        </div>
    );
}

export default Workspace;