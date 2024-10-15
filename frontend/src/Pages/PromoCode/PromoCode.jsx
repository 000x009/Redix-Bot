import React, {useState, useEffect} from 'react';
import './PromoCode.css'
import { PromoAPI, getPromo, checkIsUsedPromo } from '../../db/db';
import { useTelegram } from '../../hooks/useTelegram';

function PromoCode() {
    const [code, setCode] = useState('');
    const [validStatus, setValidStatus] = useState(0);
    const [message, setMessage] = useState('');
    const [debounceTimer, setDebounceTimer] = useState(null);
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

    useEffect(() => {
        if (validStatus === 1) {
            tg.MainButton.setText('Применить промокод');
            tg.MainButton.show();
            tg.MainButton.onClick(onSubmit);
        } else {
            tg.MainButton.hide();
        }

        return () => {
            tg.MainButton.offClick(onSubmit);
            tg.MainButton.hide();
        };
    }, [validStatus]);

    const onChange = async (e) => {
        const newCode = e.target.value;
        setCode(newCode);

        if (debounceTimer) {
            clearTimeout(debounceTimer);
        }

        if (newCode.trim() !== '') {
            const timer = setTimeout(async () => {
                const promoResult = await getPromo(newCode);
                if (promoResult) {
                    if (promoResult.uses <= 0) {
                        setValidStatus(-1);
                        setMessage('Промокод больше не действителен');
                    } else {
                        const isUsed = await checkIsUsedPromo(newCode, tg.initData);
                        if (isUsed === true) {
                            setValidStatus(-1);
                            setMessage('Промокод уже был использован вами');
                        } else {
                            setValidStatus(1);
                            setMessage('');
                        }
                    }
                } else {
                    setValidStatus(-1);
                    setMessage('Неверный промокод, попробуйте ещё раз');
                }
            }, 500);

            setDebounceTimer(timer);
        } else {
            setValidStatus(0);
            setMessage('');
        }

        if (newCode === '') {
            setValidStatus(0);
            setMessage('');
        }
    }

    const onSubmit = async () => {
        try {
            const result = await (async () => {
                console.log("api");
                const response = await PromoAPI(code, tg.initData);
                console.log("response", response);
                return response;
            })();
            if (result) {
                setValidStatus(1);
                setMessage('Промокод успешно применён');
                tg.MainButton.hide();
                window.history.back();
            } else {
                setValidStatus(-1);
                setMessage('Ошибка при применении промокода');
            }
        } catch (error) {
            setValidStatus(-1);
            setMessage('Ошибка при применении промокода');
        }
    };

    return <div>
        <div className="flex horizontal-padding vertical-padding">
            <h3>Ввести промокод</h3>
        </div>
        <div className="flex column horizontal-padding gap-1">
            <label htmlFor="code" className="subtitle">Введите промокод</label>
            <div className="flex column">
                <input id="code" value={code} onChange={onChange} name="code" placeholder="Промокод"
                       className={`input-text ${validStatus === -1 ? 'input-invalid' : ''}`}
                       type="text"/>
                <small className={`${validStatus === 1 ? 'text-valid' : 'text-invalid'}`}>{message}</small>
            </div>
        </div>
    </div>
}

export default PromoCode;