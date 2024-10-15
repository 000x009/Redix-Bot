import React from 'react';
import './Button.css';

function Button({type, title, disable, image, image_invert = false, onClick, className, ...props}) {
    return (
        <button className={`btn ${
            (type === 'add' && 'add') ||
            (type === 'remove' && 'remove') ||
            (type === 'checkout' && 'checkout') ||
            (type === 'info' && 'info') ||
            (type === 'submit' && 'submit')
        } ${className}`}
                disabled={disable}
                onClick={onClick}
                {...props}
        >
            {title}
            {image && <img style={{width: "1.3rem", alignSelf: "center", filter: `invert(${image_invert ? "1" : "0"})`}} src={image} alt=""/>}
        </button>
    );
}

export default Button;