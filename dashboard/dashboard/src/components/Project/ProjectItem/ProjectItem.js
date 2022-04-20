import React, { useContext } from 'react';

import {GlobalContext} from '../../../contexts/GlobalContext'

function ProjectItem({data}) {
    //const [info, setinfo] = useState([]);
    const {setModelParam,setProjectID, setProjectName,setProjectDataset,setResults} = useContext(GlobalContext);

    function loadProject() {
        console.log("hey")
        //setLCLID(data[0])
        fetch(`http://127.0.0.1:5000/project/` + String(data.id), {
            method: 'GET',
            headers: {
                'Content-Type': 'application.json',
            },
        }).then(
            res => res.json()
        ).then(
            data => {
                console.log(data);
                setProjectID(data.id)
                setProjectName(data.name)
                setProjectDataset(data.houses)
                if(data.mid === null){
                    setModelParam({
                        model: "",
                        training: "",
                        epoch: "",
                        lag: "",
                        layer: "",
                        prediction: ""
                    })
                    setResults("")
                }
                else{

                    console.log("aywant params and results")
                    setModelParam({
                        model: data.mtype,
                        training: data.train_test_split,
                        epoch: data.epochs,
                        lag: data.lag,
                        layer: data.layer_count,
                        prediction: ""
                    })
                    setResults(data.model_results)
                }
            }
        )

    }

    function deleteProject(){
        console.log("deleting" + String(data.id))
        fetch(`http://127.0.0.1:5000/project/` + String(data.id), {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application.json',
            },
        }).then(
            res => res.json()
        ).then(
            data => {
              console.log(data)
              loadProject() 
            }
        )
    }

    return (
        <li>
            { data.name }
            <span onClick={loadProject} className="material-icons-outlined project-icon" title="Load Project">sync</span>
            <span onClick={deleteProject} className="material-icons-outlined project-icon" title="Delete Project">delete_forever</span>
        </li>
    );
}

export default ProjectItem;