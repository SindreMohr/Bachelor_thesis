import { useState, useEffect } from 'react';

function Head({tableData}) {

    const [head, sethead] = useState("");
    
    useEffect(() => {
        console.log(head);
        console.log(tableData);
        if (tableData.head) {
            sethead(                  
                tableData.head.id.map(function(obj, i){
                    return (
                        <tr key={tableData.head.id}>
                            <td>{ tableData.head.id[i] }</td>
                            <td>{ tableData.head.lclid[i] }</td>
                            <td>{ tableData.head.tstp[i] }</td>
                            <td>{ tableData.head.energy[i] }</td>
                        </tr>
                    );
                })
            );
        };
        console.log(head);
    }, [tableData]);

    return (
        <tbody>{head}</tbody>
    );  
}

export default Head;