import './Explore.css';

import DataPlot from '../../DataPlot/DataPlot';


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
                <DataPlot />
            </div>
            <div className="Exploration-data-head">
                head
            </div>
        </div>       
    );
}

export default Explore;