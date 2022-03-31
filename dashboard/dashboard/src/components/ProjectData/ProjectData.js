import './ProjectData.css';
import {GlobalContext} from '../../contexts/GlobalContext'
import { useContext, useState, useEffect } from 'react';

function ProjectData() {
    const { ProjectID, projectDataset, setProjectDataset, LCLID } = useContext(GlobalContext);
    const [datasetList, setDatasetlist] = useState(<ul></ul>);

    function removeFromDataset(name) {
        let data = projectDataset;
        let index = data.indexOf(name);
        if (index > -1) {
            data.splice(index, 1);
        }
        setProjectDataset(data);
    }

    useEffect(() => {
        if (projectDataset[0]) {
            setDatasetlist(                  
                projectDataset.map(function(obj, i){
                    return (
                        <li key={i} >{projectDataset[i]} <span onClick={(e) => removeFromDataset(projectDataset[i])} class="material-icons-outlined">close</span></li>
                    );
                })
            );
        };
    }, [projectDataset, LCLID]);

    const clearData = event => {
        event.preventDefault();
        console.log(projectDataset);
        setProjectDataset([]);
        setDatasetlist(<ul></ul>);
    }


    return (
        <div className="ProjectData">
            <section>
                <h3>Project</h3>
                <ul>
                    <li>{ProjectID}</li>
                </ul>
            </section>
            <section>
                <h3>Dataset</h3>
                <span onClick={clearData} class="material-icons-outlined">
                    delete
                </span>
                <ul>
                    {datasetList}
                </ul>
            </section>
        </div>
    );
}

export default ProjectData;