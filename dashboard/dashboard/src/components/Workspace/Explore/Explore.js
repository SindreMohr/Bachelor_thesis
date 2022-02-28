import './Explore.css';

function Explore() {
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
                        <td>34534</td>
                    </tr>
                    <tr>
                        <td>Energy</td>
                        <td>34534</td>
                    </tr>
                    <tr>
                        <td>tstp</td>
                        <td>34534</td>
                    </tr>
                </table>
            </div>
            <div className="Exploration-plot-wrapper">
                <img src="plot.png" alt="plot" />
            </div>
            <div className="Exploration-data-head">
                name region  sales  expenses<br />
            0   William   East  50000     42000<br />
            1      Emma  North  52000     43000<br />
            2     Sofia   East  90000     50000<br />
            3    Markus  South  34000     44000<br />
            4    Edward   West  42000     38000<br />
            5    Thomas   West  72000     39000<br />
            6     Ethan  South  49000     42000<br />
            7    Olivia   West  55000     60000<br />
            8      Arun   West  67000     39000<br />
            9     Anika   East  65000     44000<br />
            10    Paulo  South  67000     45000<br />
            </div>
        </div>
    );
}

export default Explore;