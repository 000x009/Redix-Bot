import React from 'react';
import './TransactionDetail.css';
import { useEffect, useState } from 'react';
import { getOneTransaction } from '../../db/db';
import { useLocation } from 'react-router-dom';
import { useTelegram } from '../../hooks/useTelegram';
import { CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const TransactionDetail = () => {
    const [transaction, setTransaction] = useState(null);
    const [loading, setLoading] = useState(true);
    const location = useLocation();
    const transaction_id = new URLSearchParams(location.search).get("id");
    const { tg } = useTelegram();
    const navigate = useNavigate();

    useEffect(() => {
      tg.BackButton.show();
      tg.BackButton.onClick(() => {
        navigate('/profile');
      });
  
      return () => {
        tg.BackButton.offClick();
        tg.BackButton.hide();
      };
    }, []);

    useEffect(() => {
        const fetchResults = async () => {
            try {
                setLoading(true);
                const results = await getOneTransaction(transaction_id, tg.initData);
                setTransaction(results);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchResults();
      }, [transaction_id]);
    
      if (loading) return <div className="flex justify-center align-items-center" style={{height: '100vh'}}>
        <CircularProgress />
      </div>;

    return (
        <div className="transaction-detail">
            <h2>Информация о транзакции</h2>
            
            <div className="detail-item">
                <div className="label">ID транзакции</div>
                <div className="value">{transaction.id}</div>
            </div>
            
            <div className="detail-item">
                <div className="label">Дата и время транзакции</div>
                <div className="value">
                    {new Date(transaction.time).toLocaleString('ru-RU', { 
                        day: '2-digit', 
                        month: '2-digit', 
                        year: 'numeric', 
                        hour: '2-digit', 
                        minute: '2-digit', 
                        hour12: false 
                    }).replace(/[,/]/g, '.').replace(' ', ' ')}
                </div>
            </div>
            
            <div className="detail-item">
                <div className="label">Вид транзакции</div>
                <div className="value">{transaction.type}</div>
            </div>
            
            <div className="detail-item">
                <div className="label">Тип транзакции</div>
                <div className="value">{transaction.cause}</div>
            </div>
            
            <div className="detail-item">
                <div className="label">Сумма</div>
                <div className="value">{transaction.amount} ₽</div>
            </div>
        </div>
    );
};

export default TransactionDetail;