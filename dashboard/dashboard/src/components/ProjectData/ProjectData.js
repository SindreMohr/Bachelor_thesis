import './ProjectData.css';
import {GlobalContext} from '../../contexts/GlobalContext'
import { useContext, useState, useEffect } from 'react';

function ProjectData() {
    const { ProjectID, ProjectName, modelID, setModelID, projectDataset, setProjectDataset, LCLID, setPAGE, setLCLID, modelParam, setPageOverlay } = useContext(GlobalContext);
    const [datasetList, setDatasetlist] = useState(<ul></ul>);

    function removeFromDataset(name) {
        console.log(name);
        let data = projectDataset;
        let index = data.indexOf(name);
        if (projectDataset.length === 0) {
            setProjectDataset([]);
        } else if (index > -1) {
            data.splice(index, 1);
            setProjectDataset(data);
            setDatasetlist(createList());
        }
    }

    function createList() {
        let content = (
            projectDataset.map(function(obj, i){
            return (
                <li onClick={(e) => exploreData(obj)} key={i} >{obj} <span onClick={(e) => removeFromDataset(obj)} className="material-icons-outlined cross" title="Remove from dataset">close</span></li>
                );
            })
        );
        return content
    }

    function exploreData(name) {
        setLCLID(name);
        setPAGE("Explore");
    }

    const clearData = event => {
        event.preventDefault();
        setProjectDataset([]);
        setDatasetlist(<ul></ul>);
    }
    
    async function saveProject(){
        const url = "http://localhost:5000/"
        let data = {
            houses: projectDataset,
            parameters: modelParam,
            mid: modelID,
            pid: ProjectID
        }
        
        const reqOpt = {
            method: "PUT",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              data
            }),
          };
        const respons = await fetch(url + "save_project/" + String(ProjectID), reqOpt);
        const results = await respons.json();
        setModelID(results.mid)
        
       
    }

    useEffect(() => {
        if (projectDataset[0]) {
            setDatasetlist(                  
                createList()
            );
        } else {
            setDatasetlist(<ul></ul>);
        };
    }, [LCLID]);



    return (
        <div className="ProjectData">
            {ProjectName ? 
                <span>
                    <section>
                        <h2>Project Menu</h2>
                        <h3>Project: <i><b>{ProjectName}</b></i></h3>
                    </section>
                    <section>
                        <p className="project-data-title">Dataset:
                        </p>
                        <ul className="project-data-list">
                            {datasetList}
                        </ul>
                        <div className="project-edit">
                            <span onClick={saveProject} title="Save Project" className="material-icons-outlined save">
                                save
                            </span>
                            <span onClick={clearData} title="Clear Dataset" className="material-icons-outlined clear">
                                delete
                            </span>
                        </div>
                    </section>
                </span>
            :
                <span>
                    <section>
                        <h2>Project Menu</h2>
                        <p>No project loaded</p>
                        <p onClick={() => setPageOverlay("projects")}><i>Load project</i></p>
                    </section>
                </span>
            }

        </div>
    );
}

export default ProjectData;