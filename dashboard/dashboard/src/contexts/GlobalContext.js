import React, { createContext, useState } from 'react'
export const GlobalContext = createContext()
const GlobalContextProvider = (props) => {
    const [PAGE, setPAGE] = useState('Explore')
    const [LCLID, setLCLID] = useState('MAC000150')
    const [projectDataset, setProjectDataset] = useState(["MAC000150", "MAC000150"])
    const [ProjectID, setProjectID] = useState('DL_01')
    const Url = "http://localhost:3000"
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
                ProjectID,
                setProjectID,
                projectDataset,
                setProjectDataset
             }}>
               {props.children}
         </GlobalContext.Provider>
    )
}
export default GlobalContextProvider