import React from 'react';
import './Category.css';
import {useNavigate} from "react-router-dom";


function CategoryCard({item}) {
    const navigate = useNavigate();
    const {
        id,
        name,
        game,
        image_url
    } = item;

    return <div onClick={() => {
        navigate(`/category?id=${id}`)
    }} className='card horizontal-padding' >
        <div className="image_container">
            <img className='card__image' src={image_url} alt={name}/>
        </div>
        <div className="card__title">
            <h4>
                {name}
            </h4>
        </div>
        <div className="card__title">
            <small>{game}</small>
        </div>
    </div>
}

export default CategoryCard;