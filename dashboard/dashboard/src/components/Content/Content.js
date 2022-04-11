import Datamenu from '../Datamenu/Datamenu';
import Workspace from '../Workspace/Workspace';
import ProjectData from '../ProjectData/ProjectData';

import { GlobalContext } from '../../contexts/GlobalContext';
import { useContext } from 'react';

function Content() {

    const { pageOverlay } = useContext(GlobalContext);

  
    return (
      <main>
          <Datamenu />
          <Workspace />
          <ProjectData />
      </main>
    );
  }
  
  export default Content;