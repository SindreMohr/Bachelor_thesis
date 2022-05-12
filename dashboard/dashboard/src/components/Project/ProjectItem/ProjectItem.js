import React, { useContext } from 'react';

import {GlobalContext} from '../../../contexts/GlobalContext'

function ProjectItem({data}) {
    //const [info, setinfo] = useState([]);
    const {setModelParam,setModelID, ProjectID ,setProjectID, setProjectName,setProjectDataset,setResults, loadingState, setLoadingState} = useContext(GlobalContext);

    function loadProject() {
        setLoadingState(true)
        console.log(loadingState)
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
                setProjectID(data.id)
                setProjectName(data.name)
                setProjectDataset(data.houses)
                if(data.mid === null){
                    setModelID(data.mid)
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
                    setModelID(data.mid)
                    setModelParam({
                        model: data.mtype,
                        training: data.train_test_split,
                        epoch: data.epochs,
                        lag: data.lag,
                        layer: data.layer_count,
                        prediction: "0",
                        layerDictionary: data.layer_dict
                    })
                    setResults(data.model_results)
                }
            }
            )
        setLoadingState(false);
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
            output => {
              console.log(output)
              if(data.id === ProjectID){
                setProjectName();
                setProjectID();
                setProjectDataset([]);
              }
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