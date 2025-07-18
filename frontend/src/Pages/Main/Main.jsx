import React, {useState, useEffect, useMemo} from 'react';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import Card from "../../Components/Card/Card";
import Header from "../../Components/Header/Header";
import Game from "../../Components/Game/Game";
import {Dropdown} from '@mui/base/Dropdown';
import {Menu} from '@mui/base/Menu';
import {MenuButton as BaseMenuButton} from '@mui/base/MenuButton';
import {MenuItem as BaseMenuItem, menuItemClasses} from '@mui/base/MenuItem';
import {blue, grey} from "@mui/material/colors";
import {styled} from "@mui/material";
import {getGamesAPI} from "../../db/db";
import {getProducts} from "../../db/db";
import CircularProgress from '@mui/material/CircularProgress';

function Main() {
    const [games, setGamesState] = useState([]);
    const [items, setItemsState] = useState([]);
    const [sortConfig, setSortConfig] = useState({ key: 'purchase_count', direction: 'descending' });
    const [isLoading, setIsLoading] = useState(true);

    const sortValues = {
        'purchase_count': 'по популярности',
        'price_lower': 'по убыванию цены',
        'price_higher': 'по возрастанию цены',
    };
    const createHandleMenuClick = (menuItem) => {
        return () => {
          let direction = 'ascending';
          if (sortConfig.key === menuItem && sortConfig.direction === 'ascending') {
            direction = 'descending';
          }
          setSortConfig({ key: menuItem, direction });
        };
    };

    useEffect(() => {
        async function fetchData() {
            try {
                const [fetchedItems, fetchedGames] = await Promise.all([
                    getProducts(),
                    getGamesAPI()
                ]);
                setItemsState(fetchedItems);
                const filteredGames = fetchedGames.filter(game => ![15, 16, 17, 18].includes(game.id));
                setGamesState(filteredGames);
            } catch (error) {
                console.error("Error fetching data:", error);
            } finally {
                setIsLoading(false);
            }
        }
        fetchData();
    }, []);

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

    if (isLoading) {
        return (
            <div className="flex justify-center align-items-center" style={{height: '100vh'}}>
                <CircularProgress />
            </div>
        );
    }

    return <div>
        <Header/>
        <div className="flex vertical-padding horizontal-padding" style={{paddingBottom: '0.5rem'}}>
            <h2>Игры</h2>
        </div>
        <div className="flex align-stretch flex-wrap w-100">
            {games.map((game) => {
                return <Game id={game.id} name={game.name} image_url={game.image_url} key={game.id}/>;
            })}
            <Game
            id={10}
            name="Telegram"
            image_url="src/images/telegram.png"
            key={10}/>
        </div>
        <div className="flex justify-between py-08 horizontal-padding">
            <h2>Товары</h2>
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
            {sortedItems.map((item) => {
                return <Card item={item} key={item.id}/>;
            })}
        </div>
    </div>
}

export default Main;