import React, { useContext } from 'react';

import {GlobalContext} from '../../../contexts/GlobalContext'

function DatamenuItem({data}) {
    //const [info, setinfo] = useState([]);
    const { LCLID,setLCLID , Url } = useContext(GlobalContext);

    function changeLCL() {
        console.log(LCLID)
        setLCLID(data)
    }

    return (
        <li onClick={changeLCL}>
            { data }
        </li>
    );
}

export default DatamenuItem;