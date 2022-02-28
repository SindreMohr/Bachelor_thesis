import './Workspace.css';
import Workspacenav from './Workspacenav/Workspacenav';
import Explore from './Explore/Explore';

function Workspace() {
    return (
        <div className="Workspace">
           <div className="Workspace-content">
                <Workspacenav />
                <Explore />
           </div>
        </div>
    );
}

export default Workspace;