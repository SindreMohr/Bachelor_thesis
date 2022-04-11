import './Navigation.css';
import { GlobalContext } from '../../contexts/GlobalContext';
import { useContext } from 'react';


function Navigation() {

  const { setPageOverlay, pageOverlay } = useContext(GlobalContext);

  function handleClickProject() {
    console.log("projects");
    setPageOverlay("projects");
  }

  function handleClickHome() {
    console.log("projects");
    setPageOverlay();
  }

  function handleClickAbout() {
    console.log("about");
    setPageOverlay("about");
  }

  return (
    <header>
        <h1 onClick={handleClickHome}>Dashboard</h1>
        <nav>
          <ul>
            <li onClick={handleClickHome}>HOME</li>
            <li onClick={handleClickProject}>PROJECTS</li>
            <li onClick={handleClickAbout}>ABOUT</li>
          </ul>
        </nav>
    </header>
  );
}

export default Navigation;