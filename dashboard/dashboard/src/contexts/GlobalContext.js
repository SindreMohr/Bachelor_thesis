import React, { createContext, useState } from 'react'
export const GlobalContext = createContext()
const GlobalContextProvider = (props) => {
    const [LCLID, setLCLID] = useState('MAC000150')
    const Url = "http://localhost:3000"
    return (
         <GlobalContext.Provider 
            value={{
                LCLID,
                setLCLID,
                Url
             }}>
               {props.children}
         </GlobalContext.Provider>
    )
}
export default GlobalContextProvider