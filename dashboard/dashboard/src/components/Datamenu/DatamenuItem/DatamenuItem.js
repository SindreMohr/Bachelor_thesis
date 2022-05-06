import React, { useContext } from 'react';

import {GlobalContext} from '../../../contexts/GlobalContext'

function DatamenuItem({data}) {
    //const [info, setinfo] = useState([]);
    const {setLCLID, setPAGE} = useContext(GlobalContext);

    function changeLCL() {
        //console.log(LCLID)
        setLCLID(data[0]);
        setPAGE("Explore");
    }

    return (
        <li onClick={changeLCL} title="Load data">
            { data }
        </li>
    );
}

export default DatamenuItem;