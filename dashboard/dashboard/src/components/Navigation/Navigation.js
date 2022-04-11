import './Navigation.css';
import { GlobalContext } from '../../contexts/GlobalContext';
import { useContext } from 'react';


function Navigation() {

  const { setPageOverlay, pageOverlay } = useContext(GlobalContext);

  function handleClickProject() {
    console.log("projects");
    setPageOverlay("projects");
  }

  return (
    <header>
        <h1>Dashboard</h1>
        <nav>
          <ul>
            <li onClick={handleClickProject}>PROJECTS</li>
            <li><a href="#">ABOUT</a></li>
          </ul>
        </nav>
    </header>
  );
}

export default Navigation;