import React, {useState, useEffect, useMemo} from 'react';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import Card from "../../Components/Card/Card";
import {Dropdown} from '@mui/base/Dropdown';
import {Menu} from '@mui/base/Menu';
import {MenuButton as BaseMenuButton} from '@mui/base/MenuButton';
import {MenuItem as BaseMenuItem, menuItemClasses} from '@mui/base/MenuItem';
import {blue, grey} from "@mui/material/colors";
import {styled} from "@mui/material";
import {getProducts, getGame, getGamesAPI} from "../../db/db";
import { useLocation } from 'react-router-dom';
import { useTelegram } from '../../hooks/useTelegram';
import Game from "../../Components/Game/Game";
import CircularProgress from '@mui/material/CircularProgress';

function Products() {
  const [items, setItems] = useState([]);
  const [games, setGamesState] = useState([]);
  const [game_name, setGameName] = useState(null);
  const [sortConfig, setSortConfig] = useState({ key: 'purchase_count', direction: 'descending' });
  const location = useLocation();
  const category_id = new URLSearchParams(location.search).get("id");
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
    setLoading(true);

    if (category_id === '14') {
      const fetchGames = async () => {
        const data = await getGamesAPI();
        console.log(data);
        const filteredGames = data.filter(game => ['15', '16', '17', '18'].includes(game.id.toString()));
        setGamesState(filteredGames);
      };
      fetchGames();
      setLoading(false);
    }
  }, [category_id]);

  const sortValues = {
      'purchase_count': 'по популярности',
      'price_lower': 'по убыванию цены',
      'price_higher': 'по возрастанию цены',
  };

  useEffect(() => {
    setItems([]);

    if (category_id !== '14') {
      const fetchData = async () => {
        const data = await getProducts(category_id);
        setItems(data);
      };
      fetchData();
      setLoading(false);
    }
    // return () => setItems([]);
  }, [category_id]);

  useEffect(() => {
    const fetchGameName = async () => {
      const data = await getGame(category_id);
      setGameName(data.name);
    };
    fetchGameName();
  }, [category_id]);

  const sortedItems = useMemo(() => {
    let sortableItems = [...items];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        switch (sortConfig.key) {
          case 'purchase_count':
            return b.purchase_count - a.purchase_count;
          case 'price_higher':
            return a.price - b.price;
          case 'price_lower':
            return b.price - a.price;
          default:
            return 0;
        }
      });
    }
    return sortableItems;
  }, [items, sortConfig]);

  const requestSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const createHandleMenuClick = (key) => () => {
    requestSort(key);
  };

  const Listbox = styled('ul')(({theme}) => `
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 0.875rem;
  box-sizing: border-box;
  padding: 6px;
  margin: 12px 0;
  min-width: 200px;
  border-radius: 12px;
  overflow: auto;
  outline: 0px;
  background: ${theme.palette.mode === 'dark' ? grey[900] : '#fff'};
  border: 1px solid ${theme.palette.mode === 'dark' ? grey[700] : grey[200]};
  color: ${theme.palette.mode === 'dark' ? grey[300] : grey[900]};
  box-shadow: 0px 4px 6px ${theme.palette.mode === 'dark' ? 'rgba(0,0,0, 0.50)' : 'rgba(0,0,0, 0.05)'};
  z-index: 1;
  `,);

    const MenuButton = styled(BaseMenuButton)(({theme, ...props}) => `
  font-family: 'IBM Plex Sans', sans-serif;
  font-weight: 600;
  font-size: 0.875rem;
  line-height: 1.5;
  padding: 0;
  padding-left: ".2rem";
  border-radius: 8px;
  transition: all 150ms ease;
  background: var(--tg-theme-bg-color);
  cursor: pointer;
  border: none;
  display: flex;
  align-items: center;
  justify-content: end;
  user-select: none;
  &:hover {
    background: var(--tg-theme-secondary-bg-color);
    border-color: ${theme.palette.mode === 'dark' ? grey[600] : grey[300]};
  }
  `,);

  const MenuItem = styled(BaseMenuItem)(({ theme, selected }) => `
  list-style: none;
  padding: 8px;
  border-radius: 8px;
  cursor: default;
  user-select: none;

  &:last-of-type {
      border-bottom: none;
  }

  ${selected ? `
      background-color: var(--tg-theme-secondary-bg-color);
      color: var(--tg-theme-text-color);
  ` : ''}

  &:focus {
      outline: none;
      background-color: var(--tg-theme-secondary-bg-color);
      color: var(--tg-theme-text-color);
  }

  &.${menuItemClasses.disabled} {
      color: var(--tg-theme-hint-color);
    }
    `);

    if (loading) {
      return (
          <div className="flex justify-center align-items-center" style={{height: '100vh'}}>
              <CircularProgress />
          </div>
      );
    }

    if (game_id === '14') {
      return (
        <div className="flex align-stretch flex-wrap w-100">
          {games.map((game) => {
            return <Game id={game.id} name={game.name} image_url={game.image_url} key={game.id}/>;
          })}
        </div>
      );
    }

    return (
      <div>
       <div className="flex justify-between py-08 horizontal-padding">
            <h2>{game_name}</h2>
            <div className="relative">
                <Dropdown
                    sx={{
                        borderColor: "var(--tg-theme-section-separator-color) !important",
                        background: "var(--tg-theme-bg-color) !important"
                    }}>
                    <MenuButton className="text-blue">{sortValues[sortConfig.key]}<KeyboardArrowDownIcon/></MenuButton>
                    <Menu sx={{
                        color: "var(--tg-theme-text-color) !important",
                        borderColor: "var(--tg-theme-section-separator-color) !important",
                        background: "var(--tg-theme-bg-color) !important"
                        }}
                        slots={{listbox: Listbox}}>
                        {Object.entries(sortValues).map(([key, value]) => (
                            <MenuItem key={key} onClick={createHandleMenuClick(key)} selected={sortConfig.key === key}>
                                {value}
                            </MenuItem>
                        ))}
                    </Menu>
                </Dropdown>
            </div>
        </div>
        <div className="flex column">
          {sortedItems.map((item) => (
            <Card item={item} key={item.id} />
          ))}
        </div>
      </div>
    );
}

export default Products;