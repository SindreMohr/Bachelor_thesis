import './ProjectData.css';
import {GlobalContext} from '../../contexts/GlobalContext'
import { useContext, useState, useEffect } from 'react';

function ProjectData() {
    const { ProjectID, ProjectName, projectDataset, setProjectDataset, LCLID } = useContext(GlobalContext);
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
                <li key={i} >{obj} <span onClick={(e) => removeFromDataset(obj)} className="material-icons-outlined  cross">close</span></li>
                );
            })
        );
        console.log("ok")
        return content
    }

    const clearData = event => {
        event.preventDefault();
        console.log(projectDataset);
        setProjectDataset([]);
        setDatasetlist(<ul></ul>);
    }
    
    async function saveProject(){
        console.log("im saving")
        const url = "http://localhost:5000/"
        let data = {
            houses: projectDataset,
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
        console.log(results)

       
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
            <section>
                <h3>Project: {ProjectName}</h3>
            </section>
            <section>
                <h3>Dataset:
                </h3>
                <ul className="project-data-list">
                    {datasetList}
                </ul>
                <p onClick={clearData}>Clear dataset
                    <span className="material-icons-outlined">
                        delete
                    </span>
                </p>
            </section>
            <button onClick={saveProject}>Save Project</button>

        </div>
    );
}

export default ProjectData;