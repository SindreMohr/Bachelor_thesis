import './Navigation.css';

import { useContext } from 'react';

import {GlobalContext} from '../../contexts/GlobalContext';

function Navigation() {

  const { setPageOverlay } = useContext(GlobalContext);

  return (
    <header>
        <h1>Dashboard</h1>
        <nav>
          <ul>
            <li onClick={setPageOverlay("page")}>PROJECTS</li>
            <li><a href="#">ABOUT</a></li>
          </ul>
        </nav>
    </header>
  );
}

export default Navigation;