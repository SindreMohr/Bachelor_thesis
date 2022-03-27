import { useState, useEffect } from 'react';

function Head({tableData}) {

    const [head, sethead] = useState(<tr></tr>);
    
    useEffect(() => {
        console.log(tableData);
        if (tableData.head) {
            sethead(                  
                tableData.head.id.map(function(obj, i){
                    return (
                        <tr key={tableData.head.id[i]}>
                            <td>{ tableData.head.id[i] }</td>
                            <td>{ tableData.head.lclid[i] }</td>
                            <td>{ tableData.head.tstp[i] }</td>
                            <td>{ tableData.head.energy[i] }</td>
                        </tr>
                    );
                })
            );
        };
    }, [tableData]);

    return (
        <tbody>{head}</tbody>
    );  
}

export default Head;