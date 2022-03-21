import './App.css';
import Navigation from './components/Navigation/Navigation';
import Datamenu from './components/Datamenu/Datamenu';
import Workspace from './components/Workspace/Workspace';
import ProjectData from './components/ProjectData/ProjectData';

// import React, { Fragment } from 'react'
import GlobalContextProvider from './contexts/GlobalContext'


function App() {

  



  return (
    <div className="App">
      <Navigation />
      <main>
        <GlobalContextProvider>
          <Datamenu />
          <Workspace />
          <ProjectData />
        </GlobalContextProvider>
      </main>
    </div>
  );
}

export default App;
