import './App.css';
import Navigation from './components/Navigation/Navigation';
import Footer from './components/Footer/Footer';

import Datamenu from './components/Datamenu/Datamenu';
import Workspace from './components/Workspace/Workspace';
function App() {
  return (
    <div className="App">
      <Navigation />
      <main>
         <Datamenu />
         <Workspace />
      </main>
    </div>
  );
}

export default App;
