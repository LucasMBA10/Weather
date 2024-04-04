import React from "react";
import './TempInfo.css';

function TempInfo() {
    return (
        <div className="TempContainer">
            <span>

                <div className="Cidade">
                    <h1>Sorocaba</h1>
                    <h1> 19 C </h1>
                </div>
                <div className="Condição">
                    <h1>Nublado</h1>
                    <h2>Vento: 20 km/h </h2>
                    <h3>Umidade: Y%</h3>
                </div>
            </span>
        </div>
    )
}

export default TempInfo