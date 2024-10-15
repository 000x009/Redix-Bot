import React, { useState } from 'react';
import './SearchBar.css';
import search from '../../images/search.png';
import {useNavigate} from "react-router-dom";


const debounce = (func, delay) => {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => func.apply(this, args), delay);
    };
};


export function SearchBar({ onSearch, initialValue = '' }) {
    const navigate = useNavigate();
    const theme = window.Telegram.WebApp.colorScheme;
    const [searchTerm, setSearchTerm] = useState(initialValue);
  
    const handleInputChange = (e) => {
      const term = e.target.value;
      setSearchTerm(term);
      onSearch(term);
    };
  
    return (
      <div className="search__container">
        <img style={{filter: `invert(${theme === 'dark' ? "1" : "0"})`}} className='search__icon' src={search} alt=""/>
        <input
          placeholder='Искать игру или товар...'
          className="search__bar"
          type="text"
          value={searchTerm}
          onChange={handleInputChange}
          onClick={() => navigate('/search')}
        />
      </div>
    );
  }