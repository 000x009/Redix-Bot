import React from 'react';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTelegram } from '../../hooks/useTelegram';

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
    <div className="flex flex-col min-h-screen p-4 bg-tg-theme-bg-color text-tg-theme-text-color">
      <h1 className="text-xl font-bold mb-auto">Заказ создан!</h1>
      <div className="flex-grow flex flex-col items-center justify-center">
        <div className="mb-8">
          <svg className="w-16 h-16 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <p className="text-center mb-8">Мы получили ваш заказ!</p>
        <button 
          onClick={handleReturnToProfile}
          style={{
            backgroundColor: 'var(--tg-theme-button-color)',
            color: 'var(--tg-theme-button-text-color)',
            padding: '0.5rem 1rem',
            borderRadius: '0.25rem',
            border: 'none',
            cursor: 'pointer'
          }}
        >
          Вернуться в профиль
        </button>
      </div>
    </div>
  );
};

export default OrderCreated;