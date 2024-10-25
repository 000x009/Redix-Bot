import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MainButton } from '@vkruglikov/react-telegram-web-app';
import { getOneProduct, sendOrder } from '../../db/db';
import { useTelegram } from '../../hooks/useTelegram';

const OrderForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [emailError, setEmailError] = useState('');
  const [codeSuccess, setCodeSuccess] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [twoFactorCode, setTwoFactorCode] = useState('');
  const [formFields, setFormFields] = useState([]);
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [formErrors, setFormErrors] = useState({});
  const [pubg_id, setPubgId] = useState('');
  const [blockman_id, setBlockmanId] = useState('');
  const [nickname, setNickname] = useState('');
  const [login, setLogin] = useState('');
  const { tg } = useTelegram();
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
 
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

  const isCooldownPassed = (productId) => {
    const lastOrderTime = localStorage.getItem(`lastOrder_${productId}`);
    if (!lastOrderTime) return true;
    const timePassed = Date.now() - parseInt(lastOrderTime);
    return timePassed > 10000;
  };

  useEffect(() => {
    if (!id) {
      setLoading(false);
      return;
    }

    const fetchProduct = async () => {
      try {
        const fetchedProduct = await getOneProduct(id);
        setProduct(fetchedProduct);

        switch(fetchedProduct.game_id) {
          case 1:
          case 2:
          case 3:
          case 4:
          case 15:
          case 16:
          case 17:
          case 18:
            setFormFields(['email', 'code']);
            break;
          case 5:
            setFormFields(['username', 'password', 'twoFactorCode']);
            break;
          case 10:
            setFormFields(['nickname']);
            break;
          case 7:
            setFormFields(['pubg_id']);
            break;
          case 6:
          case 8:
          case 9:
          case 11:
          case 12:
            setFormFields(['email', 'password']);
            break;
          case 13:
            setFormFields(['blockman_id']);
            break;
          default:
            setFormFields(['login', 'password']);
        }
      } catch (error) {
        console.error('Error fetching product:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchProduct();
  }, [id]);

  const handleEmailSubmit = () => {
    if (!email.trim()) {
      setEmailError('Пожалуйста, заполните поле email');
      setCodeSuccess('');
      return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
      setEmailError('Такой почты не существует');
      setCodeSuccess('');
    } else {
      setEmailError('');
      setCodeSuccess('Код был успешно отправлен');
      // Здесь должна быть логика отправки кода
    }
  };

  const handleSubmit = async () => {
    if (isSubmitting || !isCooldownPassed(id)) {
      alert('Пожалуйста, подождите. Заказ уже обрабатывается или не прошло 10 секунд с предыдущего заказа.');
      return;
    }
  
    const errors = {};
    formFields.forEach(field => {
      if (field !== 'twoFactorCode' && !eval(field)) {
        errors[field] = true;
      }
    });
  
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      alert('Пожалуйста, заполните все обязательные поля');
      return;
    }
  
    setIsSubmitting(true);
  
    try {
      let additionalData = {};
      switch(product.game_id) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 15:
        case 16:
        case 17:
        case 18:
          additionalData = { email, code };
        break;
        case 5:
          additionalData = { login: username, password, two_factor_code: twoFactorCode || null };
          break;
        case 12:
          additionalData = { login: email, password };
          break;
        case 10:
          additionalData = { nickname };
          break;
        case 7:
          additionalData = { pubg_id };
          break;
        case 6:
        case 8:
        case 9:
        case 11:
          additionalData = { login: email, password };
          break;
        case 13:
          additionalData = { blockman_id, password };
          break;
        default:
          additionalData = { login, password };
      }
      await sendOrder(id, additionalData, tg.initData);
      localStorage.setItem(`lastOrder_${id}`, Date.now().toString());
      navigate('/order/success');
    } catch (error) {
      console.error('Error sending order:', error);
      alert('Произошла ошибка при отправке заказа');
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderFormFields = () => {
    return formFields.map((field) => {
      const commonInputStyle = {
        width: '100%',
        padding: '0.5rem',
        borderRadius: '0.25rem',
        color: 'var(--tg-theme-text-color)',
        backgroundColor: 'var(--tg-theme-secondary-bg-color)',
        boxSizing: 'border-box',
        maxWidth: '100%',
        border: 'none',
        borderBottom: '1px solid var(--tg-theme-hint-color)',
        outline: 'none',
        fontSize: '16px'
      };
      
      switch(field) {
        case 'email':
          return ( 
            <div key={field} style={{marginBottom: '1rem'}}>
              <label style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem'}}>
                {product.game_id === 8 ? 'Почта от Facebook/Google Play' :
                 product.game_id === 9 || product.game_id === 6 ? 'Почта от XBOX Live' :
                 product.game_id === 11 ? 'Почта' :
                 product.game_id === 12 ? 'Почта' :
                 product.game_id === 1 || product.game_id === 2 || product.game_id === 3 || product.game_id === 4 || product.game_id === 15 || product.game_id === 16 || product.game_id === 17 || product.game_id === 18 ? 'Почта' : 'Почта Supercell ID'}
              </label>
              <div style={{display: 'flex'}}>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  style={{
                    ...commonInputStyle,
                    flexGrow: 1,
                    borderTopRightRadius: 0,
                    borderBottomRightRadius: 0,
                    borderBottom: formErrors.email ? '1px solid red' : '1px solid var(--tg-theme-hint-color)'
                  }}
                  placeholder="Введите email"
                />
                {(product.game_id === 1 || product.game_id === 2 || product.game_id === 3 || product.game_id === 4) && (
                  <button
                    onClick={handleEmailSubmit}
                    style={{backgroundColor: '#3b82f6', color: 'white', padding: '0.5rem', borderTopRightRadius: '0.25rem', borderBottomRightRadius: '0.25rem', border: 'none'}}
                  >
                    ➤
                  </button>
                )}
              </div>
              {(product.game_id === 1 || product.game_id === 2 || product.game_id === 3 || product.game_id === 4) && (
                <p style={{color: 'gray', fontSize: '0.75rem', marginTop: '0.25rem'}}>Стрелка отправляет код Supercell ID на почту</p>
              )}
              {emailError && <p style={{color: '#ef4444', fontSize: '0.875rem', marginTop: '0.25rem'}}>{emailError}</p>}
              {codeSuccess && <p style={{color: '#10b981', fontSize: '0.875rem', marginTop: '0.25rem'}}>{codeSuccess}</p>}
            </div>
          );
        case 'code':
          return (
            <div key={field} style={{marginBottom: '1rem'}}>
              <label style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem'}}>Код</label>
              <input
                type="text"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                style={{
                  ...commonInputStyle,
                  borderBottom: formErrors.code ? '1px solid red' : '1px solid var(--tg-theme-hint-color)'
                }}
                placeholder="Введите код"
              />
            </div>
          );
        case 'username':
          return (
            <div key={field} style={{marginBottom: '1rem'}}>
              <label style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem'}}>Имя пользователя</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                style={{
                  ...commonInputStyle,
                  borderBottom: formErrors.username ? '1px solid red' : '1px solid var(--tg-theme-hint-color)'
                }}
                placeholder="Введите имя пользователя"
              />
            </div>
          );
          case 'password':
            return (
              <div key={field} style={{marginBottom: '1rem'}}>
                <label style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem'}}>
                  {product.game_id === 8 ? 'Пароль от Facebook/Google Play' :
                   product.game_id === 9 ? 'Пароль от XBOX Live' :
                   'Пароль'}
                </label>
                <div style={{position: 'relative'}}>
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{
                      ...commonInputStyle,
                      borderBottom: formErrors.password ? '1px solid red' : '1px solid var(--tg-theme-hint-color)',
                      paddingRight: '2.5rem'
                    }}
                    placeholder="Введите пароль"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    style={{
                      position: 'absolute',
                      right: '0.5rem',
                      top: '50%',
                      transform: 'translateY(-50%)',
                      background: 'none',
                      border: 'none',
                      cursor: 'pointer',
                      padding: 0,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}
                  >
                    {showPassword ? (
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{width: '20px', height: '20px'}}>
                        <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                        <line x1="1" y1="1" x2="23" y2="23"></line>
                      </svg>
                    ) : (
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{width: '20px', height: '20px'}}>
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    )}
                  </button>
                </div>
              </div>
            );
        case 'twoFactorCode':
          return (
            <div key={field} style={{marginBottom: '1rem'}}>
              <label style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem'}}>Код двухфакторной аутентификации (необязательно)</label>
              <input
                type="text"
                value={twoFactorCode}
                onChange={(e) => setTwoFactorCode(e.target.value)}
                style={{
                  ...commonInputStyle,
                  borderBottom: '1px solid var(--tg-theme-hint-color)'
                }}
                placeholder="Введите код двухфакторной аутентификации"
              />
              <p style={{color: 'gray', fontSize: '0.75rem', marginTop: '0.25rem'}}>
                Укажите двухфакторный код, если у вас подключена 2-х факторная аутентификация по почте/аутентификатору. Если у вас она не подключена, то просто оставьте это поле пустым.
              </p>
            </div>
          );
        case 'nickname':
          return (
            <div key={field} style={{marginBottom: '1rem'}}>
              <label style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem'}}>
                {product.game_id === 12 ? 'Ник (советую скопировать его, очень важно написать его верно)' : 'Никнейм'}
              </label>
              <input
                type="text"
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
                style={{
                  ...commonInputStyle,
                  borderBottom: formErrors.nickname ? '1px solid red' : '1px solid var(--tg-theme-hint-color)'
                }}
                placeholder="Введите никнейм"
              />
            </div>
          );
        case 'pubg_id':
          return (
            <div key={field} style={{marginBottom: '1rem'}}>
              <label style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem'}}>
                PUBG ID
              </label>
              <input
                type="text"
                value={pubg_id}
                onChange={(e) => setPubgId(e.target.value)}
                style={{
                  ...commonInputStyle,
                  borderBottom: formErrors.pubg_id ? '1px solid red' : '1px solid var(--tg-theme-hint-color)'
                }}
                placeholder="Введите PUBG ID"
              />
            </div>
          );
        case 'blockman_id':
          return (
            <div key={field} style={{marginBottom: '1rem'}}>
              <label style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem'}}>
                Ваш ID
              </label>
              <input
                type="text"
                value={blockman_id}
                onChange={(e) => setBlockmanId(e.target.value)}
                style={{
                  ...commonInputStyle,
                  borderBottom: formErrors.blockman_id ? '1px solid red' : '1px solid var(--tg-theme-hint-color)'
                }}
                placeholder="Введите ID"
              />
            </div>
          );
        case 'login':
          return (
            <div key={field} style={{marginBottom: '1rem'}}>
              <label style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem'}}>Логин</label>
              <input
                type="text"
                value={login}
                onChange={(e) => setLogin(e.target.value)}
                style={{
                  ...commonInputStyle,
                  borderBottom: formErrors.login ? '1px solid red' : '1px solid var(--tg-theme-hint-color)'
                }}
                placeholder="Введите логин"
              />
            </div>
          );
        default:
          return null;
      }
    });
  };

  if (loading) {
    return (
      <div style={{minHeight: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: 'var(--tg-theme-bg-color)', color: 'var(--tg-theme-text-color)'}}>
        <p>Загрузка...</p>
      </div>
    );
  }

  if (!id) {
    return (
      <div style={{minHeight: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: 'var(--tg-theme-bg-color)', color: 'var(--tg-theme-text-color)'}}>
        <p>Ошибка: ID товара не определен в OrderProcessing</p>
      </div>
    );
  }

  const makeLinksClickable = (text) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.split(urlRegex).map((part, index) => 
      urlRegex.test(part) ? <a key={index} href={part} target="_blank" rel="noopener noreferrer">{part}</a> : part
    );
  };

  return (
    <div style={{minHeight: '100vh', display: 'flex', flexDirection: 'column', padding: '1rem', backgroundColor: 'var(--tg-theme-bg-color)', color: 'var(--tg-theme-text-color)', overflow: 'hidden', maxWidth: '100vw'}}>
      <h1 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem'}}>Оформление заказа</h1>
      <div style={{flexGrow: 1, display: 'flex', flexDirection: 'column'}}>
        {(product.instruction_image_url || (product.instruction && product.instruction.trim() !== '')) && (
          <div className="bg-lightgray rounded px-08 py-08" style={{ marginBottom: '1.5rem' }}>
            {product.instruction_image_url && (
              <img 
                src={product.instruction_image_url} 
                alt="Instruction" 
                style={{width: '100%', maxHeight: '200px', objectFit: 'cover', marginBottom: '1rem'}}
              />
            )}
            {product.instruction && product.instruction.trim() !== '' && (
              <div className="word-pre" style={{ marginTop: product.instruction_image_url ? '1rem' : '0' }}>
                {makeLinksClickable(product.instruction)}
              </div>
            )}
          </div>
        )}
        {renderFormFields()}
      </div>
      <MainButton text={isSubmitting ? "Обработка..." : "Продолжить"} onClick={handleSubmit} disabled={isSubmitting} />
    </div>
  );
}

export default OrderForm;