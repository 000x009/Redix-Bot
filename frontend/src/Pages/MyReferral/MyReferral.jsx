import React, {useState, useEffect} from 'react';
import './MyReferral.css'
import Button from "../../Components/Button";
import { getUser, checkCodeAvailability, setReferralCode } from '../../db/db';
import { useTelegram } from '../../hooks/useTelegram';
import CircularProgress from '@mui/material/CircularProgress';

function MyReferral() {
    const [code, setCode] = useState('');
    const [validStatus, setValidStatus] = useState(0);
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [btnMessage, setBtnMessage] = useState('Копировать ссылку');
    const [link, setLink] = useState(`https://t.me/paradoxxx_test_bot?start=${code}`);
    const [user, setUser] = useState(null);
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
        const fetchUser = async () => {
            const response = await getUser(tg.initData);
            setUser(response);
            setCode(response.referral_code);
            setLink(`https://t.me/paradoxxx_test_bot?start=${response.referral_code}`);
        };
        fetchUser();
        setIsLoading(false);
    }, []);

    useEffect(() => {
        tg.MainButton.setText("Сохранить");
        tg.MainButton.onClick(onSubmit);
        if (code.trim() !== '') {
            tg.MainButton.show();
        } else {
            tg.MainButton.hide();
        }

        return () => {
            tg.MainButton.offClick();
            tg.MainButton.hide();
        };
    }, [code]);

    const onChange = (e) => {
        const newCode = e.target.value;
        const allowedChars = /^[a-zA-Z0-9]*$/;
        if (!allowedChars.test(newCode)) {
            setValidStatus(-1);
            setMessage('Разрешены только английские буквы и цифры');
            return;
        }
        setCode(newCode);
        
        if (newCode.trim() === '') {
            setValidStatus(-1);
            setMessage('Реферальный код не может быть пустым');
            return;
        }
        
        const checkAvailability = async () => {
            const response = await checkCodeAvailability(newCode);
            if (response) {
                if (newCode === user.referral_code) {
                    setValidStatus(0);
                    setMessage('');
                } else {
                    setValidStatus(1);
                    setMessage('Реферальный код доступен');
                }
            } else {
                if (newCode !== user.referral_code) {
                    setValidStatus(-1);
                    setMessage('Реферальный код уже занят другим пользователем');
                } else {
                    setValidStatus(0);
                    setMessage('');
                }
            }
        }
        
        checkAvailability();
    }

    const onSubmit = async () => {
        if (code.trim() === '') {
            setValidStatus(-1);
            setMessage('Реферальный код не может быть пустым');
            return;
        }
        setLink(`https://t.me/paradoxxx_test_bot?start=${code}`);
        try {
            if (code !== user.referral_code) {  
                await setReferralCode(code, tg.initData);
                setValidStatus(1);
                setMessage('Готово!');
                setUser(prevUser => ({...prevUser, referral_code: code}));
            } else {
                setValidStatus(-1);
                setMessage('Реферальный код уже занят вами');
            }
        } catch (error) {
            setValidStatus(-1);
            setMessage('Ошибка при установке реферального кода');
        }
    }

    const onCopy = (text) => {
        navigator.clipboard.writeText(text);
        setBtnMessage('Ссылка скопирована')
    }

    if (isLoading) {
        return (
            <div className="flex justify-center align-items-center" style={{height: '100vh'}}>
                <CircularProgress />
            </div>
        );
    }

    return <div>
        <div className="flex horizontal-padding vertical-padding">
            <h3>Реферальная программа</h3>
        </div>
        <div className="flex column horizontal-padding gap-1">
            <div className="label" style={{marginBottom: '0.5rem'}}>Ваш реферальный код:</div>
            <div className="flex column">
                <input id="code" value={code} onChange={onChange} name="code" placeholder={code}
                       className={`input-text ${validStatus === 1 && 'input-valid'} ${validStatus === -1 && 'input-invalid'}`}
                       type="text"
                       style={{marginBottom: '0.5rem'}}/>
                <small className={`${validStatus === 1 ? 'text-valid' : 'text-invalid'}`} style={{marginBottom: '0.5rem'}}>{message}</small>
            </div>
        </div>
        <div className="horizontal-padding flex column">
            <div className="label" style={{marginBottom: '0.5rem'}}>Распространяйте ваше реферальную ссылку, и за
                каждого нового пользователя по вашей ссылке
                вы будете получать процент с каждой его покупки на баланс.
            </div>

            <span className="fw-500">Ваша реферальная ссылка:</span>
            <p className="text-wrap"><code>{link}</code></p>
            <Button onClick={() => {
                onCopy(link)
            }} style={{color: "red !important"}} className="w-100 text__center"
                    type="secondary"
                    title={btnMessage}></Button>
        </div>
    </div>
}

export default MyReferral;