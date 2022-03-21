import React, { useContext } from 'react';

import {GlobalContext} from '../../../contexts/GlobalContext'

function DatamenuItem({data}) {
    //const [info, setinfo] = useState([]);
    const { LCLID, Url } = useContext(GlobalContext);

    function changeLCL() {
        console.log("f" +LCLID +"f")
    }

    return (
        <li onClick={changeLCL}>
            { data }
        </li>
    );
}

export default DatamenuItem;