import React, {useState, useEffect} from 'react';
import {getCategories} from "../../db/db";
import { useLocation } from 'react-router-dom';
import { useTelegram } from '../../hooks/useTelegram';
import { Category as CategoryCard } from '../../Components/Category/Category';
import CircularProgress from '@mui/material/CircularProgress';

function Category() {
  const [items, setItems] = useState([]);
  const location = useLocation();
  const game_id = new URLSearchParams(location.search).get("id");
  const { tg } = useTelegram();
  const [loading, setLoading] = useState(true);

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

  useEffect(() => {
    setItems([]);

    const fetchData = async () => {
        const data = await getCategories(game_id);
        setItems(data);
    };
    fetchData();
    setLoading(false);
    return () => setItems([]);
  }, [game_id]);

    if (loading) {
      return (
          <div className="flex justify-center align-items-center" style={{height: '100vh'}}>
              <CircularProgress />
          </div>
      );
    }

    return (
      <div className="flex column">
        <div className="flex column">
          {items.map((item) => (
            <CategoryCard item={item} key={item.id} />
          ))}
        </div>
      </div>
    );
}

export default Category;