import './Explore.css';


function Explore() {
    let lclid = 123123;
    let energy = 12341234;
    let tstp = 12341234;
    return (
        <div className="Exploration-view">
            <div className="Exploration-table-wrapper">
                <table className="Exploration-table">
                    <thead>
                        <td>Column</td>
                        <td>Count</td>
                    </thead>
                    <tr>
                        <td>LCLID</td>
                        <td>{ lclid }</td>
                    </tr>
                    <tr>
                        <td>Energy</td>
                        <td>{ energy }</td>
                    </tr>
                    <tr>
                        <td>tstp</td>
                        <td>{ tstp }</td>
                    </tr>
                </table>
            </div>
            <div className="Exploration-plot-wrapper">
                <img src="plot.png" alt="plot" />
            </div>
            <div className="Exploration-data-head">

            </div>
        </div>
    );
}

export default Explore;