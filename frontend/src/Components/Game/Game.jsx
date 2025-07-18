import React from 'react';
import './Game.css';
import { useNavigate } from "react-router-dom";

function Game({ id, name, image_url }) {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate(`/game?id=${id}`);
    };

    return (
        <div onClick={handleClick} className='card__1x1 vertical-padding horizontal-padding'>
            <img className='card__1x1__image' src={image_url} alt={name} />
            <div className="card__1x1__title text__center">
                <span className="mt-05">
                    {name}
                </span>
            </div>
        </div>
    );
}

export default Game;