import React from 'react';
import './Card.css';
import {useNavigate} from "react-router-dom";


function Card({item}) {
    const navigate = useNavigate();

    if (item.name === "Telegram Stars") {
        return <div onClick={() => {
            navigate('/telegram-stars', {state: {categoryId: item.id}});
        }} className='card horizontal-padding' >
            <div className="image_container">
                <img className='card__image' src={item.image_url} alt={item.name}/>
            </div>
            <div className="card__title">
                <h4>
                    {item.name}
                </h4>
            </div>
        </div>
    }

    return <div onClick={() => {
        navigate(`/product/${item.id}`)
    }} className='card horizontal-padding' >
        <div className="image_container">
            <img className='card__image' src={item.image_url} alt={item.name}/>
        </div>
        <div className="card__title">
            <h4>
                {item.name}
                {item.purchase_limit && ` (Осталось в наличии: ${item.purchase_limit - item.purchase_count})`}
            </h4>
            <h4>{item.price} ₽</h4>
        </div>
    </div>
}

export default Card;