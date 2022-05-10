import React, { createContext, useState } from 'react'
export const GlobalContext = createContext()
const GlobalContextProvider = (props) => {
    const [PAGE, setPAGE] = useState('Explore')
    const [LCLID, setLCLID] = useState('MAC000150')
    const [projectDataset, setProjectDataset] = useState([])
    const [ProjectID, setProjectID] = useState(0)
    const [modelID, setModelID] = useState(null)
    const [loadingState, setLoadingState] = useState(false);

    const [ProjectName, setProjectName] = useState()

    const [Results, setResults] = useState("");
    const Url = "http://localhost:3000"
    const [pageOverlay, setPageOverlay] = useState("");
    const [modelParam, setModelParam] = useState(
        {
            model: "",
            training: "",
            epoch: "",
            lag: "",
            layer: "",
            prediction: ""
        }
        )
    const [saveData, setSaveData] = useState();
    return (
         <GlobalContext.Provider 
            value={{
                PAGE,
                setPAGE,
                LCLID,
                setLCLID,
                Url,
                modelParam,
                setModelParam,
                modelID,
                setModelID,
                ProjectID,
                setProjectID,
                ProjectName,
                setProjectName,
                projectDataset,
                setProjectDataset,
                Results,
                setResults,
                pageOverlay,
                setPageOverlay,
                saveData,
                setSaveData,
                loadingState,
                setLoadingState,
             }}>
               {props.children}
         </GlobalContext.Provider>
    )
}
export default GlobalContextProvider