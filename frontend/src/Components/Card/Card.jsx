import React, {useState} from 'react';
import './Card.css';
import starFilled from '../../images/star.png';
import starOutlined from '../../images/star_outlined.png';
import {useNavigate} from "react-router-dom";


function Card({item}) {
    const navigate = useNavigate();
    const {
        id,
        name,
        description,
        price,
        game_id,
        instruction,
        purchase_count,
        game,
        category,
        image_url
    } = item;

    return <div onClick={() => {
        navigate(`/product/${id}`)
    }} className='card horizontal-padding' >
        <div className="image_container">
            <img className='card__image' src={image_url} alt={name}/>
        </div>
        <div className="card__title">
            <h4>
                {name}
            </h4>
            <h4>{price} ₽</h4>
        </div>
        <div className="card__title">
            <small>{game}</small>
        </div>
    </div>
}

export default Card;