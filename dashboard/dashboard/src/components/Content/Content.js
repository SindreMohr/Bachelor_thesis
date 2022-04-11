import Datamenu from '../Datamenu/Datamenu';
import Workspace from '../Workspace/Workspace';
import ProjectData from '../ProjectData/ProjectData';

import { GlobalContext } from '../../contexts/GlobalContext';
import { useContext } from 'react';
import Project from '../Project/Project';

function Content() {

    const { pageOverlay } = useContext(GlobalContext);

  
    return (
      <div>
          { pageOverlay === "projects" ?
          <main>
              Projects
              <Project/>
          </main>
          : pageOverlay === "about" ?
          <main>
              About
          </main>
          :
          <main>
              <Datamenu />
              <Workspace />
              <ProjectData />
          </main>
            }
      </div>
    );
  }
  
  export default Content;