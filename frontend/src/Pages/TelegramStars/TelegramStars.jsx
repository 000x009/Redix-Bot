import React, { useState, useEffect } from 'react';
import './TelegramStars.css';
import { useTelegram } from '../../hooks/useTelegram';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useLaunchParams } from '@telegram-apps/sdk-react';
import { getStarsConfig } from '../../db/db';
import { buyStars } from '../../db/db';

const API_URL = "http://localhost:8000/api";
const MIN_STARS = 50;
const MAX_STARS = 1000000;

function TelegramStars() {
    const {tg, user} = useTelegram();
    const [amount, setAmount] = useState();
    const [rate, setRate] = useState(1.5);
    const [username, setUsername] = useState('');
    const [showPopup, setShowPopup] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const { launchParams } = useLaunchParams();

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

    // Эффект для управления MainButton
    useEffect(() => {
        tg.MainButton.setParams({
            text: 'Купить Telegram Stars',
            color: '#2481cc',
        });

        const isValid = !error && amount && amount >= MIN_STARS && amount <= MAX_STARS && username.trim();

        if (isValid) {
            tg.MainButton.show();
        } else {
            tg.MainButton.hide();
        }

        // Обработчик нажатия на MainButton
        const handleMainButtonClick = () => {
            setShowPopup(true);
        };

        tg.MainButton.onClick(handleMainButtonClick);

        return () => {
            tg.MainButton.offClick(handleMainButtonClick);
            tg.MainButton.hide();
        };
    }, [amount, error, username]);

    useEffect(() => {
        const fetchRate = async () => {
            try {
                const response = await getStarsConfig();
                setRate(response.data.rate);
            } catch (error) {
                console.error('Error fetching rate:', error);
            }
        };
        fetchRate();
    }, []);

    const handleAmountChange = (value) => {
        // Удаляем все нецифровые символы
        const numericValue = value.replace(/[^0-9]/g, '');
        
        if (numericValue === '') {
            setAmount('');
            setError('Введите количество звезд');
            return;
        }

        const numberValue = parseInt(numericValue, 10);

        if (numberValue < MIN_STARS) {
            setAmount(numericValue);
            setError(`Минимальное количество звезд: ${MIN_STARS}`);
            return;
        }

        if (numberValue > MAX_STARS) {
            setAmount(MAX_STARS);
            setError(`Максимальное количество звезд: ${MAX_STARS}`);
            return;
        }

        setAmount(numberValue);
        setError('');
    };

    const handleBuyClick = async () => {
        try {
            const response = await buyStars(username, amount);
            
            if (response.data.insufficient_balance) {
                setShowPopup(false);
                navigate('/deposit');
                return;
            }
            
            // Закрываем попап после успешной покупки
            setShowPopup(false);
            // Можно добавить уведомление об успешной покупке
            tg.showAlert('Звезды успешно куплены!');
        } catch (error) {
            console.error('Error purchasing stars:', error);
            if (error.response?.data?.insufficient_balance) {
                setShowPopup(false);
                navigate('/deposit');
            } else {
                // Показываем ошибку пользователю
                tg.showAlert('Произошла ошибка при покупке звезд. Попробуйте позже.');
            }
        }
    };

    useEffect(() => {
        console.log("Launch params", launchParams);
    }, [launchParams]);

    return (
        <div className="telegram-stars-container">
            <div className="header">
                <h1>⭐ REDIX</h1>
                <p>Покупайте Telegram Stars дешевле</p>
            </div>

            <div className="current-rate">
                Текущий курс: {rate}₽ за звезду
            </div>

            <div className="recipient-section">
                <h3>Выберите получателя</h3>
                <div className="for-me-link" onClick={() => setUsername(user.username)}>
                    Для меня @{user.username}
                </div>
                <input 
                    type="text" 
                    placeholder="Введите username Telegram..." 
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="username-input"
                />
            </div>

            <div className="amount-section">
                <h3>Выберите количество Telegram Stars</h3>
                <input 
                    type="text"
                    value={amount}
                    onChange={(e) => handleAmountChange(e.target.value)}
                    placeholder={`от ${MIN_STARS} до ${MAX_STARS} звезд`}
                    className="amount-input"
                />
                {error && <div className="error-message">{error}</div>}
            </div>

            <div className="disclaimer">
                <input type="checkbox" id="disclaimer" required />
                <label htmlFor="disclaimer">
                    Я покупаю Telegram Stars для себя или в подарок друзьям. Я НЕ оплачиваю товары или услуги на других сайтах или платформах от имени незнакомцев.
                </label>
            </div>

            {showPopup && (
                <div className="telegram-popup" onClick={() => setShowPopup(false)}>
                    <div className="telegram-popup-content" onClick={e => e.stopPropagation()}>
                        <h2>Купить Telegram Stars</h2>
                        <p className="stars-amount">Вы покупаете {amount} Telegram Stars</p>
                        <div className="recipient-message">
                            <p>Получатель получит подобное сообщение:</p>
                            <div className="gift-message">
                                <p className="sender">Кое-кто</p>
                                <p>отправил вам подарок</p>
                                <div className="gift-box">
                                    <img src="/telegram-gift-box.png" alt="Подарок" />
                                    <p>{amount} Telegram Stars</p>
                                    <p className="gift-description">для активации контента и сервисов</p>
                                </div>
                            </div>
                        </div>
                        <div className="popup-buttons">
                            <button 
                                className="telegram-button"
                                onClick={handleBuyClick}
                            >
                                Купить звёзды для @{username}
                            </button>
                            <button 
                                className="telegram-button secondary"
                                onClick={() => setShowPopup(false)}
                            >
                                Отмена
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default TelegramStars; 