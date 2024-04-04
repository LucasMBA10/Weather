import React from "react";
import './Search.css'
import { useState } from "react";


const APIkey = '8394d96233c9c56df8c68a745da0945a'


function Search() {
    // Logica

    const [value, setValue] = useState('')
    const [city, setCity] = useState('')

    let url = `https://api.openweathermap.org/data/2.5/weather?q=${value}&appid=${APIkey}`

    

    const getInput = (evento) => {
        setValue(evento.target.value)
    }

    const search = () => {
        setValue(value)
        setCity(value)
        request()
    }

    const request = () => { 

        fetch(url).then(res => res.json()).then((json) => {
            console.log(json)
        }).catch((error) => {
            console.log(error)
        })
    }

    return (

        <div className="SearchContainer">
            <span>
                <input type="text" onChange={getInput} value={value} name="" className="SearchInput" id="" />
                <input type="button" onClick={search} className="SearchButton" value={"Buscar"} />
            </span>
        </div>
    )
}

export default Search