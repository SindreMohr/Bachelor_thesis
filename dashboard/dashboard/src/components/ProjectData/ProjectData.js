import './ProjectData.css';
import {GlobalContext} from '../../contexts/GlobalContext'
import { useContext, useState, useEffect } from 'react';

function ProjectData() {
    const { ProjectID, projectDataset, setProjectDataset, LCLID } = useContext(GlobalContext);
    const [datasetList, setDatasetlist] = useState(<ul></ul>);

    function removeFromDataset(name) {
        console.log(name);
        let data = projectDataset;
        let index = data.indexOf(name);
        if (projectDataset.length === 0) {
            setProjectDataset([]);
        } else if (index > -1) {
            data.splice(index, 1);
        }
        setProjectDataset(data);
    }
    const clearData = event => {
        event.preventDefault();
        console.log(projectDataset);
        setProjectDataset([]);
        setDatasetlist(<ul></ul>);
    }

    useEffect(() => {
        if (projectDataset[0]) {
            setDatasetlist(                  
                projectDataset.map(function(obj, i){
                    return (
                        <li key={i} >{projectDataset[i]} <span onClick={(e) => removeFromDataset(projectDataset[i])} className="material-icons-outlined  cross">close</span></li>
                    );
                })
            );
        } else {
            setDatasetlist(<ul></ul>);
        };
    }, [removeFromDataset]);



    return (
        <div className="ProjectData">
            <section>
                <h3>Project: {ProjectID}</h3>
            </section>
            <section>
                <h3>Dataset:
                </h3>
                <ul className="project-data-list">
                    {datasetList}
                </ul>
                <span onClick={clearData} className="material-icons-outlined">
                    delete
                </span>
            </section>
        </div>
    );
}

export default ProjectData;