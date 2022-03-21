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
                        <td>Mean</td>
                        <td>Std.</td>
                        <td>Min.</td>
                        <td>Max.</td>
                    </thead>

                    <tr>
                        <td>Energy</td>
                        <td>{ energy }</td>
                        <td>{ lclid }</td>
                        <td>{ lclid }</td>
                        <td>{ lclid }</td>
                        <td>{ lclid }</td>
                    </tr>
                    <tr>
                        <td>Date</td>
                        <td>{ tstp }</td>
                        <td>{ lclid }</td>
                        <td>{ lclid }</td>
                        <td>{ lclid }</td>
                        <td>{ lclid }</td>
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