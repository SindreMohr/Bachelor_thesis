import React, { useContext } from 'react';

import {GlobalContext} from '../../../contexts/GlobalContext'

function DatamenuItem({data}) {
    //const [info, setinfo] = useState([]);
    const { LCLID, Url } = useContext(GlobalContext);
    function sayYo() {
        console.log(Url);
        setLCLID(data);
        console.log("f" +LCLID +"f")
    }

    return (
        <li onClick={sayYo}>
            { data }
            { LCLID }
        </li>
    );
}

export default DatamenuItem;