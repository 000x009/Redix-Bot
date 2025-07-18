import React from 'react';
import './CategoryCard.css';
import {useNavigate} from "react-router-dom";


function CategoryCard({item}) {
    const navigate = useNavigate();
    const {
        id,
        game_id,
        name,
        image,
        is_visible,
        thread_id
    } = item;

    return <div onClick={() => {
        if (name === "Звезды") {
            navigate('/telegram-stars');
        } else {
            navigate(`/category?id=${id}`)
        }
    }} className='card horizontal-padding' >
        <div className="image_container">
            <img className='card__image' src={image} alt={name}/>
        </div>
        <div className="card__title">
            <h4>
                {name}
            </h4>
        </div>
        {/* <div className="card__title">
            <small>{game}</small>
        </div> */}
    </div>
}

export default CategoryCard;