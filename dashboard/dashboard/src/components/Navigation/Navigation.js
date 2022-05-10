import './Navigation.css';
import { GlobalContext } from '../../contexts/GlobalContext';
import { useContext } from 'react';


function Navigation() {

  const { setPageOverlay, pageOverlay } = useContext(GlobalContext);

  function handleClickProject() {
    setPageOverlay("projects");
  }

  function handleClickHome() {
    setPageOverlay();
  }

  function handleClickAbout() {
    setPageOverlay("about");
  }

  return (
    <header>
        <h1 onClick={handleClickHome}>
          <span className="material-icons-outlined bolt">
            bolt
          </span>
          Deep Learning Dashboard
        </h1>
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