import './Project.css';
import ProjectItem from './ProjectItem/ProjectItem';

import { useState, useEffect, useContext } from 'react';

import {GlobalContext} from '../../contexts/GlobalContext'

function Project() {
    
    const [projectList, setProjectList] = useState([]);
    const [projectItems, setProjectItems] = useState([]);

    //for initing empty project
    const {setProjectID, ProjectName, setProjectName, setProjectDataset, loadingState} = useContext(GlobalContext);

    //form
    const [nameValue, setNameValue] = useState("Untitled project");


    useEffect(() => {
        fetch(`http://127.0.0.1:5000/projects`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application.json',
            }
        }).then(
            res => res.json(),
        ).then(
            data => {
                setProjectList(data.projects);
                //setProjectItems(createProjectList());
            }
        )

        //console.log(projectList)
    }, []);

    function createList() {
        let projectItems = projectList.map((d) =>  <ProjectItem key={d.id} data={d} />);
        return projectItems;
    }

    useEffect(() => {
        if (projectList[0]) {
            const values = createList();
            setProjectItems(values);
        } else {
            setProjectItems([]);
        }
    }, [projectList, ProjectName, setProjectItems])

    function exitProject() {
        setProjectName();
        setProjectID();
        setProjectDataset([]);
    }


    async function postForm(){
        const url = "http://localhost:5000/"
        let data = {
            name: nameValue,
        }
        
        const reqOpt = {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              data
            }),
          };
        const respons = await fetch(url + "projects", reqOpt);
        const results = await respons.json();
        console.log(results);
        //making new project current project
        // //data.id makes it problematic as that it null ... 
        // setProjectID(data.id)
        // setProjectName(data.name)
        // setProjectDataset([])
             
        // setModelParam({
        //     model: "",
        //     training: "",
        //     epoch: "",
        //     lag: "",
        //     layer: "",
        //     prediction: ""
        //         })
        // setResults("")
    }


    let loadedProject = (
        <ul className='project-list'>
            <li>
                {ProjectName}
                <span></span>
                <span onClick={exitProject} className="material-icons-outlined project-icon" title="Exit Project">close</span>
            </li>
        </ul>
    );

    return (
        <div className='project-wrapper'>
            <div className='project-content'>
                <h2>Projects</h2>
                <h3>Current Project:</h3>
                {loadingState ?
                "Loading project"
                :ProjectName && !loadingState ? loadedProject
                : "No project loaded"}

                <h3>Saved Projects:</h3>
                <ul className='project-list'>
                    {projectItems}
                </ul>


                <h3>Create New Project:</h3>
                <label>
                    <input id="name" type="text" value={nameValue}  onChange={(e) => setNameValue(e.target.value)}/>
                </label>
                <button onClick={postForm}>Create</button>
            </div>
        </div>       



    );
}

export default Project;