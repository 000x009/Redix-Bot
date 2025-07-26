import React, { useState, useEffect, useRef } from 'react';
import './TelegramStars.css';
import { useTelegram } from '../../hooks/useTelegram';
import { useNavigate, useLocation } from 'react-router-dom';
import { useLaunchParams } from '@telegram-apps/sdk-react';
import { getStarsConfig, getUser } from '../../db/db';
import { buyStars } from '../../db/db';
import { CircularProgress } from '@mui/material';
import Lottie from "lottie-react"
import GiftAnimation from "../../images/gift.json"

const MIN_STARS = 50;
const MAX_STARS = 1000000;

function TelegramStars() {
    const {tg, user} = useTelegram();
    const [amount, setAmount] = useState();
    const [rate, setRate] = useState(0);
    const [username, setUsername] = useState('');
    const [showPopup, setShowPopup] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const { launchParams } = useLaunchParams();
    const [dbUser, setDbUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [buyLoading, setBuyLoading] = useState(false);
    const location = useLocation();
    const categoryId = location.state?.categoryId;
    const starRef = useRef(null);

    useEffect(() => {
        async function fetchUser() {
            try {
                const userData = await getUser(tg.initData);
                setDbUser(userData);
            } catch (error) {
                console.error("Error fetching user data:", error);
            } finally {
                setLoading(false);
            }
        }
        fetchUser();
    }, [tg]);

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
        const fetchRate = async () => {
            try {
                const response = await getStarsConfig();
                setRate(response.rate);
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
            const totalCost = amount * rate;
            if (dbUser && dbUser.balance < totalCost) {
                const deficiencyAmount = totalCost - dbUser.balance;
                navigate('/deficiency/1', { 
                    state: { 
                        deficiencyAmount: deficiencyAmount
                    }
                });
                return;
            }
            setShowPopup(true);
        };

        tg.MainButton.onClick(handleMainButtonClick);

        return () => {
            tg.MainButton.offClick(handleMainButtonClick);
            tg.MainButton.hide();
        };
    }, [amount, error, username, rate, dbUser, navigate]);

    const handleBuyClick = async () => {
        if (buyLoading) return; // Prevent multiple clicks
        
        setBuyLoading(true);
        try {
            const totalCost = amount * rate;
            if (dbUser && dbUser.balance < totalCost) {
                const deficiencyAmount = totalCost - dbUser.balance;
                setShowPopup(false);
                setBuyLoading(false);
                navigate('/deficiency-balance', { 
                    state: { 
                        deficiencyAmount: deficiencyAmount
                    }
                });
                return;
            }
            console.log(categoryId)
            const response = await buyStars(username, amount, categoryId, tg.initData);
            setShowPopup(false);
            tg.showAlert('Звезды успешно куплены!');
        } catch (error) {
            console.error('Error purchasing stars:', error);
            tg.showAlert('Произошла ошибка при покупке звезд. Попробуйте позже.');
        } finally {
            setBuyLoading(false);
        }
    };

    useEffect(() => {
        console.log("Launch params", launchParams);
    }, [launchParams]);

    if (loading) {
        return (
            <div className="flex justify-center align-items-center" style={{height: '100vh'}}>
                <CircularProgress />
            </div>
        );
    }

    return (
        <div className="telegram-stars-container">
            <div className="header">
                <h1>⭐ Redix Shop</h1>
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
                {amount && rate && (
                    <div className="total-cost">
                        Итого к оплате: {(amount * rate).toFixed(2)}₽
                    </div>
                )}
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
                                    <Lottie
                                        animationData={GiftAnimation}
                                        lottieRef={starRef}
                                        loop={false}
                                        autoplay={true}
                                        style={{
                                            width: "150px",
                                            height: "150px",
                                            cursor: "pointer",
                                            // transform: "translateX(50%)",
                                            marginLeft: "66px",
                                        }}
                                        onClick={() => {
                                            starRef.current.goToAndPlay(0);
                                        }}
                                    />
                                    <p>{amount} Telegram Stars</p>
                                    <p className="gift-description">для активации контента и сервисов</p>
                                </div>
                            </div>
                        </div>
                        <div className="popup-buttons">
                            <button 
                                className="telegram-button"
                                onClick={handleBuyClick}
                                disabled={buyLoading}
                                style={{
                                    opacity: buyLoading ? 0.6 : 1,
                                    cursor: buyLoading ? 'not-allowed' : 'pointer'
                                }}
                            >
                                {buyLoading ? 'Обработка...' : `Купить звёзды для @${username}`}
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