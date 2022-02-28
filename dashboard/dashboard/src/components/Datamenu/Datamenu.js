import './Datamenu.css';

let visible = true;

function toggleVisibility() {
    visible = !visible;
    console.log(visible);
}

function Datamenu() {
    return (
        <div className="Datamenu">
            <h2>Data</h2>
            <div className="Datamenu-content">
                + halfhourly <input type="checkbox"></input><br />
                + daily <input type="checkbox"></input><br />
            </div>
        </div>
    );
}

export default Datamenu;