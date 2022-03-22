import { useState, useEffect, useContext } from 'react';

import GlobalContextProvider, {GlobalContext} from '../../../contexts/GlobalContext'

function Modify() {

    const { LCLID } = useContext(GlobalContext);
  
    return (
        <div className="Exploration-view">
            <div className="Exploration-table-wrapper">
                <div className="">
                    <h2> Modify {LCLID} </h2>

                </div>
            </div>
        
            <div className="Exploration-plot-wrapper">
            </div>
            <div className="Exploration-data-head">
                
            </div>
        </div>       
    );
}

export default Modify;