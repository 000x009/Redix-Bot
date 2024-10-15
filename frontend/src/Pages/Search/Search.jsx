import React, { useState } from 'react';
import { SearchBar } from '../../Components/SearchBar/SearchBar';
import { useTelegram } from '../../hooks/useTelegram';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Search.css';

export function SearchPage() {
    const { tg } = useTelegram();
    const navigate = useNavigate();
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        tg.BackButton.show();
        tg.BackButton.onClick(() => {
            window.history.back();
        });

        return () => {
            tg.BackButton.offClick();
            tg.BackButton.hide();
        };
    }, [tg.BackButton]);

    const handleSearch = (term) => {
        setSearchTerm(term);
        if (term.trim() !== '') {
            navigate(`/search?query=${encodeURIComponent(term)}`);
        }
    };

    return (
        <div className="search-page">
            <div className="header">
                <SearchBar onSearch={handleSearch} initialValue={searchTerm} />
            </div>
        </div>
    );
}