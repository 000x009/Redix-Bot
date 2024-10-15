import React, { useEffect, useState, useMemo } from "react";
import { searchProducts } from '../../db/db';
import Card from "../../Components/Card/Card";
import { SearchBar } from "../../Components/SearchBar/SearchBar";
import { useTelegram } from "../../hooks/useTelegram";
import './SearchProducts.css';
import CircularProgress from '@mui/material/CircularProgress';

export const SearchProducts = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  const { tg } = useTelegram();

  useEffect(() => {
    tg.BackButton.show();
    tg.BackButton.onClick(() => {
      window.history.back();
    });

    return () => {
      tg.BackButton.offClick();
      tg.BackButton.hide();
    };
  }, []);

  const handleSearch = async (term) => {
    setSearchTerm(term);
    if (term.trim() === '') {
      setSearchResults([]);
      return;
    }
    setLoading(true);
    try {
      const results = await searchProducts(term);
      setSearchResults(results);
    } catch (error) {
      console.error("Error fetching search results:", error);
      setSearchResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="header">
        <SearchBar onSearch={handleSearch} />
      </div>
      {loading ? (
        <div className="flex justify-center align-items-center" style={{height: '100vh'}}>
          <CircularProgress />
        </div>
      ) : (
        <div className="flex column">
          {searchResults.length > 0 && (
            searchResults.map((item) => (
              <Card 
                sx={{
                  '&:hover': {
                    backgroundColor: "var(--tg-theme-secondary-bg-color)"
                  }
                }} 
                item={item} 
                key={item.id}
              />
            ))
          )}
        </div>
      )}
    </div>
  );
};