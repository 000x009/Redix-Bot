import React from 'react';
import './Header.css';
import Button from "../Button";
import profile from '../../images/profile.png';
import starOutlined from '../../images/star_outlined.png';
import { useNavigate } from "react-router-dom";
import { SearchBar } from '../SearchBar/SearchBar';


export default function Header() {
    const theme = window.Telegram.WebApp.colorScheme;
    const navigate = useNavigate();

    const handleSearchClick = (term) => {
        if (term.trim() !== '') {
            navigate(`/search?query=${encodeURIComponent(term)}`);
        } else {
            navigate('/search');
        }
    };

    return (
        <div className='header'>
            <SearchBar 
                onSearch={handleSearchClick} 
                onClick={() => navigate('/search')} 
                style={{ width: '100%', maxWidth: '850px' }}
            />
            <Button image_invert={theme === 'dark'} image={starOutlined} onClick={() => navigate('/feedbacks')} />
            <Button image_invert={theme === 'dark'} image={profile} onClick={() => navigate('/profile')} />
        </div>
    );
}