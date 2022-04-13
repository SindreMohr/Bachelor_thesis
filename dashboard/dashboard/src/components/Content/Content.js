import Datamenu from '../Datamenu/Datamenu';
import Workspace from '../Workspace/Workspace';
import ProjectData from '../ProjectData/ProjectData';

import { GlobalContext } from '../../contexts/GlobalContext';
import { useContext } from 'react';
import Project from '../Project/Project';
import About from '../About/About';

function Content() {

    const { pageOverlay } = useContext(GlobalContext);

  
    return (
      <div>
          { pageOverlay === "projects" ?
          <main>
              <Project/>
          </main>
          : pageOverlay === "about" ?
          <main>
              <About />
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