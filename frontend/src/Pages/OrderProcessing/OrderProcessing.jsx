import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MainButton } from '@vkruglikov/react-telegram-web-app';
import { getOneProduct, sendOrder, getOneCategory, verifyTag } from '../../db/db';
import { useTelegram } from '../../hooks/useTelegram';

const OrderForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formFields, setFormFields] = useState({});
  const [product, setProduct] = useState(null);
  const [category, setCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [formErrors, setFormErrors] = useState({});
  const { tg } = useTelegram();
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [emailError, setEmailError] = useState('');
  const [codeSuccess, setCodeSuccess] = useState('');
  const [tagVerificationMessage, setTagVerificationMessage] = useState('');
  const [tagVerificationSuccess, setTagVerificationSuccess] = useState(false);
 
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

    const fetchProductAndCategory = async () => {
      try {
        const fetchedProduct = await getOneProduct(id);
        setProduct(fetchedProduct);
        const fetchedCategory = await getOneCategory(fetchedProduct.category_id);
        setCategory(fetchedCategory);
        
        const initialFormFields = {};
        fetchedCategory.required_fields.forEach(field => {
          initialFormFields[field] = '';
        });
        setFormFields(initialFormFields);
      } catch (error) {
        console.error('Error fetching product or category:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchProductAndCategory();
  }, [id]);

  const handleEmailSubmit = () => {
    if (!formFields.почта || !formFields.почта.trim()) {
      setEmailError('Пожалуйста, заполните данное поле');
      setCodeSuccess('');
      return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(formFields.почта)) {
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
    Object.keys(formFields).forEach(field => {
      if (field !== 'two_factor_code' && !formFields[field]) {
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
      await sendOrder(id, formFields, tg.initData);
      localStorage.setItem(`lastOrder_${id}`, Date.now().toString());
      navigate('/order/success');
    } catch (error) {
      console.error('Error sending order:', error);
      alert('Произошла ошибка при отправке заказа');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleVerifyTag = async (tag) => {
    try {
      const result = await verifyTag(tag);
      if (result.exists) {
        setTagVerificationMessage('Тег существует!');
        setTagVerificationSuccess(true);
      } else {
        setTagVerificationMessage('Тег не найден');
        setTagVerificationSuccess(false);
      }
    } catch (error) {
      console.error('Error verifying tag:', error);
      setTagVerificationMessage('Ошибка при проверке тега');
      setTagVerificationSuccess(false);
    }
  };

  const renderFormFields = () => {
    if (!category || !category.required_fields) return null;

    return category.required_fields.map((field) => {
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
      
      const handleInputChange = (e) => {
        setFormFields(prev => ({...prev, [field]: e.target.value}));
      };

      let label = field.charAt(0).toUpperCase() + field.slice(1).replace('_', ' ');
      let placeholder = `Введите ${label.toLowerCase()}`;

      if (field === 'почта') {
        label = 'Почта';
        placeholder = 'Введите почту';
      } else if (field === 'пароль') {
        label = 'Пароль';
        placeholder = 'Введите пароль';
      }

      if (field === 'почта') {
        return ( 
          <div key={field} style={{marginBottom: '1rem'}}>
            <label style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem'}}>
              {label}
            </label>
            <div style={{display: 'flex'}}>
              <input
                type="email"
                value={formFields[field]}
                onChange={handleInputChange}
                style={{
                  ...commonInputStyle,
                  flexGrow: 1,
                  borderTopRightRadius: 0,
                  borderBottomRightRadius: 0,
                  borderBottom: formErrors[field] ? '1px solid red' : '1px solid var(--tg-theme-hint-color)'
                }}
                placeholder={placeholder}
              />
              <button
                onClick={handleEmailSubmit}
                style={{backgroundColor: '#3b82f6', color: 'white', padding: '0.5rem', borderTopRightRadius: '0.25rem', borderBottomRightRadius: '0.25rem', border: 'none'}}
              >
                ➤
              </button>
            </div>
            <p style={{color: 'gray', fontSize: '0.75rem', marginTop: '0.25rem'}}>Стрелка отправляет код на почту</p>
            {emailError && <p style={{color: '#ef4444', fontSize: '0.875rem', marginTop: '0.25rem'}}>{emailError}</p>}
            {codeSuccess && <p style={{color: '#10b981', fontSize: '0.875rem', marginTop: '0.25rem'}}>{codeSuccess}</p>}
          </div>
        );
      } else if (field === 'пароль') {
        return (
          <div key={field} style={{marginBottom: '1rem'}}>
            <label style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem'}}>
              {label}
            </label>
            <div style={{position: 'relative'}}>
              <input
                type={showPassword ? "text" : "password"}
                value={formFields[field]}
                onChange={handleInputChange}
                style={{
                  ...commonInputStyle,
                  borderBottom: formErrors[field] ? '1px solid red' : '1px solid var(--tg-theme-hint-color)',
                  paddingRight: '2.5rem'
                }}
                placeholder={placeholder}
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
      } else if (field === 'тег') {
        return (
          <div key={field} style={{marginBottom: '1rem'}}>
            <label style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem'}}>
              {label}
            </label>
            <input
              type="text"
              value={formFields[field]}
              onChange={handleInputChange}
              style={{
                ...commonInputStyle,
                borderBottom: formErrors[field] ? '1px solid red' : '1px solid var(--tg-theme-hint-color)'
              }}
              placeholder={placeholder}
            />
            <button
              onClick={() => handleVerifyTag(formFields[field])}
              style={{
                color: '#3b82f6',
                background: 'none',
                border: 'none',
                padding: '0.5rem 0',
                cursor: 'pointer',
                fontSize: '0.875rem'
              }}
            >
              Проверить тег
            </button>
            {tagVerificationMessage && (
              <p style={{
                color: tagVerificationSuccess ? '#10b981' : '#ef4444',
                fontSize: '0.875rem',
                marginTop: '0.25rem'
              }}>
                {tagVerificationMessage}
              </p>
            )}
          </div>
        );
      } else {
        return (
          <div key={field} style={{marginBottom: '1rem'}}>
            <label style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem'}}>
              {label}
            </label>
            <input
              type="text"
              value={formFields[field]}
              onChange={handleInputChange}
              style={{
                ...commonInputStyle,
                borderBottom: formErrors[field] ? '1px solid red' : '1px solid var(--tg-theme-hint-color)'
              }}
              placeholder={placeholder}
            />
          </div>
        );
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
        {renderFormFields()}
      </div>
      <MainButton text={isSubmitting ? "Обработка..." : "Продолжить"} onClick={handleSubmit} disabled={isSubmitting} />
    </div>
  );
}

export default OrderForm;