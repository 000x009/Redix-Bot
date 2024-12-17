import React, { useState, useEffect, useCallback } from 'react';
import { getOneProduct, getUser } from '../../db/db';
import { useParams } from 'react-router-dom';
import { useTelegram } from '../../hooks/useTelegram';
import CircularProgress from '@mui/material/CircularProgress';
import { makeDeposit } from '../../db/db';
import { useNavigate } from 'react-router-dom';
import './DeficiencyDeposit.css';

const DeficiencyDeposit = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [method, setMethod] = useState(36);
    const [amount, setAmount] = useState('');
    const [validStatus, setValidStatus] = useState(0);
    const [message, setMessage] = useState('');
    const [dbUser, setDbUser] = useState(null);
    const { tg } = useTelegram();

    useEffect(() => {
        const fetchProduct = async () => {
            if (!id) {
                console.error("Product ID is undefined");
                setLoading(false);
                return;
            }
            try {
                const product = await getOneProduct(id);
                setProduct(product);
            } catch (error) {
                console.error("Error fetching product:", error);
            } finally {
                setLoading(false);
            }
        }
        fetchProduct();
    }, [id]);  
    
    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await getUser(tg.initData);
                setDbUser(response);
                if (product) {
                    const requiredAmount = Math.max(product.price - response.balance, 0);
                    setAmount(requiredAmount.toString());
                    handleChangeAmount({ target: { value: requiredAmount.toString() } });
                }
            } catch (error) {
                console.error("Error fetching user:", error);
            }
        }
        fetchUser();
    }, [product])

    const handleMainButtonClick = useCallback(async () => {
        const response = await makeDeposit(amount, method, tg.initData);
        navigate(`/payment/${response.id}`);
    }, [amount, method, tg, navigate]);

    useEffect(() => {
        const isValidAmount = amount && parseInt(amount) >= 10 && parseInt(amount) <= 50000;
        
        tg.MainButton.setText('Оплатить');
        
        if (isValidAmount) {
            tg.MainButton.show();
            tg.MainButton.onClick(handleMainButtonClick);
        } else {
            tg.MainButton.hide();
        }

        return () => {
            tg.MainButton.offClick(handleMainButtonClick);
            tg.MainButton.hide();
        };
    }, [amount, tg.MainButton, handleMainButtonClick]);
 
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

    const handleChangeAmount = (e) => {
        let val = parseInt(e.target.value);
        if (isNaN(val) || val < 10) {
            setValidStatus(-1);
            setMessage('Минимальная сумма - 10 руб!')
        } else if (val > 50000) {
            setValidStatus(-1);
            setMessage('Максимальная сумма - 50000 руб!')
        } else {
            setValidStatus(1);
            setMessage('')
        }
        setAmount(e.target.value)
    }

    if (loading || !dbUser) {
        return (
            <div className="flex justify-center align-items-center" style={{height: '100vh'}}>
                <CircularProgress />
            </div>
        );
    }

    return <div>
        <div className="flex horizontal-padding vertical-padding">
            <h3>Пополнить баланс</h3>
        </div>
        <div className="flex column horizontal-padding gap-1">
            <div className="error-message">
                <h2 style={{color: 'red'}}>Ой!</h2>
                <p>❌ Недостаточно средств на балансе!</p>
                <p>Ваш баланс: {dbUser.balance} ₽</p>
                {product && <p>Необходимо пополнить баланс на {Math.max(product.price - dbUser.balance, 0)} ₽</p>}
            </div>
            <label htmlFor="amount" className="subtitle">Введите сумму в рублях</label>
            <div className="flex column">
                <input 
                    id="amount" 
                    value={amount} 
                    onChange={handleChangeAmount} 
                    name="amount" 
                    placeholder="Сумма"
                    className={`input-text ${validStatus === 1 ? 'input-valid' : ''} ${validStatus === -1 ? 'input-invalid' : ''}`}
                    type="number" 
                    min={10} 
                    max={50000}
                />
                <small className={`${validStatus === 1 ? 'text-valid' : 'text-invalid'}`}>{message}</small>
            </div>
            <div className="flex column gap-2">
                <h3>Выберите способ оплаты</h3>
                <div className="flex gap-1 align-items-center">
                    <input checked={method === 36} id="card" name="type" type="radio" onChange={() => setMethod(36)}/>
                    <label htmlFor="card">Картой (Kassa)</label>
                </div>
                <div className="flex gap-1 align-items-center">
                    <input id="sbp" name="type" type="radio" onChange={() => setMethod(44)}/>
                    <label htmlFor="sbp">СБП (Kassa)</label>
                </div>
            </div>
        </div>
    </div>
};

export default DeficiencyDeposit;