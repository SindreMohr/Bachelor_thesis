import './About.css';

function About() {

    return (
        <div className='about-wrapper'>
            <div className='about-content'>
                <h2>Deep Learning Dashboard</h2>
                <p>
                    <b>Authors:</b> Daniel Havstad, Danny Vo, Sindre Mohr
                    <br />
                    <b>Date edited:</b> 17. Apr. 2022
                </p>
                <p>
                    Sliter du med å gå gjennom og analysere strømbruken for et nabolag? Er du lei av å gå gjennom data? Da har du kommet til riktig sted! Ved hjelp av maskinlæring trenger du ikke tenke på å måtte ta en all nighter lenger, 
                    send dataen inn i modellen og la den bruke sin magi. Lag en kopp kaffe, len deg tilbake og vent på resultatene.
                    <br />
                    <br />
                    Vi er studenter i 3rd året på UiS. Som bachelor oppgave har vi fått tildelt dette spennende prosjektet som går ut på å forecaste strømforbruk. 
                </p>
                <p>
                    Text approved by all members :D
                </p>
            </div>
        </div>       
    );
}

export default About;