import './Project.css';
import { useState, useEffect, useContext } from 'react';

import {GlobalContext} from '../../contexts/GlobalContext'

function Project() {
    
    const [projectList, setProjectList] = useState([]);
    const [projectItems, setProjectItems] = useState("");

    useEffect(() => {
        console.log("im running")
        fetch(`http://127.0.0.1:5000/projects`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application.json',
            }
        }).then(
            res => res.json(),
            console.log(res)


        ).then(
            data => {
                setProjectList(data.projects);
                setProjectItems(createProjectList());
            }
        )

        console.log(projectList)
    }, []);

    function createProjectList() {
        let content = (
            projectList.map(function(obj, i){
            return (
                <li key={i} >{obj.name}</li>
                );
            })
        );
        return content
    }

    return (
        <div>
            <ul>
                {projectItems}
            </ul>
        </div>       
    );
}

export default Project;