import './About.css';

function About() {

    return (
        <div className='about-wrapper'>
            <div className='about-content'>
                <h2>Deep Learning Dashboard</h2>
                <p>
                    <b>Authors:</b> Daniel Havstad, Danny Vo, Sindre Mohr
                    <br />
                    <b>Date edited:</b> 12. May 2022
                </p>
                <p>
                The project uses models for predictions of electricity consumption for households in London. There are many algorithms that can be used in machine learning models, the ones we have chosen to take a closer look at LSTM, Perceptron, SLP, MLP, decision tree and linear regression. Using different models makes it easier to compare predictions and find out which ones are most accurate. The measurements of electricity consumption in the thesis come from smart meters in London (5566 households), between 2011 and 2014. The measurements are made every half hour and are measured in kilowatt hours. The houses are divided into different categories, and in this project we have chosen houses in the category affluent, which want the "ordinary" households.
                <br />
                <br />
                The machine learning part of the project is written in python and uses the Tensorflow and Scikit-learn libraries. Python is a popular and modern programming language that is user-friendly. Python is especially widely used in machine learning projects, as they are often iterative.
                <br />
                <br />
                A web application is an application that runs in users' browsers, and is delivered by servers where the code is up to date. Python was also used to write the backend to the web application, which is a short distance from the models for use in the application. More specifically, it was written with Flask, which is a micro-framework for web applications in python. Server communicates with client via API, which is a way to send information between backend and frontend. Frontend was written in React.js with html and css. React is a tool used to create user interfaces and is not a framework, but is a JavaScript library. A database based on SQLite was written for storing information.
                    <br />
                    <br />
                    This application was made as a Bachelor thesis project at the University of Stavanger.
                </p>
            </div>
        </div>       
    );
}

export default About;