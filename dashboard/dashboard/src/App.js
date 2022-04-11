import './App.css';
import Navigation from './components/Navigation/Navigation';
import GlobalContextProvider from './contexts/GlobalContext'

import Content from './components/Content/Content';

function App() {
  return (
    <div className="App">
      <GlobalContextProvider>
        <Navigation />
        <Content />
      </GlobalContextProvider>
    </div>
  );
}

export default App;