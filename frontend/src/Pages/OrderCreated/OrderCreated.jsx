import React from 'react';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTelegram } from '../../hooks/useTelegram';
import './OrderCreated.css';

const OrderCreated = () => {
  const navigate = useNavigate();
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

  const handleReturnToProfile = () => {
    navigate('/profile');
  };

  return (
    <div className="order-created-container">
      <h1 className="order-created-title">Заказ создан!</h1>
      <div className="order-created-content">
        <div className="order-created-icon-container">
          <svg className="order-created-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <p className="order-created-message">Мы получили ваш заказ!</p>
        <button 
          onClick={handleReturnToProfile}
          className="order-created-button"
        >
          Вернуться в профиль
        </button>
      </div>
    </div>
  );
};

export default OrderCreated;