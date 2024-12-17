import React, {useState, useEffect} from 'react';
import './Deposit.css'
import { makeDeposit } from '../../db/db';
import { useNavigate } from 'react-router-dom';
import { useTelegram } from '../../hooks/useTelegram';

function Deposit() {
    const navigate = useNavigate();
    const [amount, setAmount] = useState('');
    const [method, setMethod] = useState(36);
    const [validStatus, setValidStatus] = useState(0);
    const [message, setMessage] = useState('');
    const { tg } = useTelegram();

    useEffect(() => {
        document.querySelector('meta[http-equiv="Cache-Control"]').setAttribute("content", "no-cache, no-store, must-revalidate");
        document.querySelector('meta[http-equiv="Pragma"]').setAttribute("content", "no-cache");
        document.querySelector('meta[http-equiv="Expires"]').setAttribute("content", "0");
    }, []);
 
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
    
    const onChange = (e) => {
        let val = parseInt(e.target.value);
        if (val < 10) {
            setValidStatus(-1);
            setMessage('Минимальная сумма - 10 руб!')
        } else if (val > 50000) {
            setValidStatus(-1);
            setMessage('Максимальная сумма - 50000 руб!')
        } else {
            setValidStatus(0);
            setMessage('')
        }
        setAmount(e.target.value)
    }

    const onSubmit = async () => {
        if (validStatus === -1 || !amount) {
            tg.showAlert('Пожалуйста, введите корректную сумму');
            return;
        }
        const response = await makeDeposit(amount, method, tg.initData);
        navigate(`/payment/${response.id}`, { replace: true });
    };

    useEffect(() => {
        tg.MainButton.setParams({
            text: 'Оплатить',
            color: '#2cab37',
        });
        tg.MainButton.onClick(onSubmit);
        tg.MainButton.show();
    
        return () => {
            tg.MainButton.offClick(onSubmit);
            tg.MainButton.hide();
        };
    }, [amount, method, validStatus]);

    return <div>
        <div className="flex horizontal-padding vertical-padding">
            <h3>Пополнить баланс</h3>
        </div>
        <div className="flex column horizontal-padding gap-1">
            <label htmlFor="amout" className="subtitle">Введите сумму в рублях</label>
            <div className="flex column">
                <input id="amout" value={amount} onChange={onChange} name="amout" placeholder="Сумма"
                       className={`input-text ${validStatus === 1 && 'input-valid'} ${validStatus === -1 && 'input-invalid'}`}
                       type="number" min={10} max={50000}/>
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
}

export default Deposit;