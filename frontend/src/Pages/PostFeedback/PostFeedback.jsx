import React, { useState, useEffect, useCallback } from 'react';
import './PostFeedback.css';
import { useParams } from 'react-router-dom';
import { postFeedback, getOneProduct, isUserPostedFeedback, getOneOrder } from '../../db/db';
import { useNavigate } from 'react-router-dom';
import { useTelegram } from '../../hooks/useTelegram';
import CircularProgress from '@mui/material/CircularProgress';

const PostFeedback = () => {
  const [rating, setRating] = useState(5);
  const [review, setReview] = useState('');
  const [product, setProduct] = useState(null);
  const [order, setOrder] = useState(null);
  const [error, setError] = useState('');
  const [isWebApp, setIsWebApp] = useState(false);
  const { id } = useParams();
  const navigate = useNavigate();
  const { tg } = useTelegram();
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [photos, setPhotos] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    setIsWebApp(!!window.Telegram?.WebApp);
  }, []);

  useEffect(() => {
    if (isWebApp) {
      tg.BackButton.show();
      tg.BackButton.onClick(() => navigate(-1));
  
      return () => {
        tg.BackButton.offClick(() => navigate(-1));
        tg.BackButton.hide();
      };
    }
  }, [tg.BackButton, navigate, isWebApp]);

  const handleSubmit = useCallback(async () => {
    if (isSubmitting) return;
    
    setError('');
    if (review.trim() === '') {
      setShowConfirmation(true);
    } else {
      submitReview();
    }
  }, [review, product, rating, tg.initData, navigate, photos, isSubmitting]);
  
  const submitReview = async () => {
    if (isSubmitting) return;
    
    setIsSubmitting(true);
    try {
      const is_posted = await isUserPostedFeedback(id, tg.initData);
      if (is_posted) {
        setError('Вы уже оставили отзыв на этот товар');
      } else {
        const photoFiles = await Promise.all(photos.map(async (photoUrl) => {
          const response = await fetch(photoUrl);
          const blob = await response.blob();
          return new File([blob], `photo_${Date.now()}.jpg`, { type: 'image/jpeg' });
        }));
        await postFeedback(order.id, product.id, rating, review.trim(), photoFiles, tg.initData);
        navigate('/');
      }
    } catch (err) {
      console.error('Error submitting review:', err);
      setError('Произошла ошибка при отправке отзыва. Пожалуйста, попробуйте еще раз.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handlePhotoUpload = async (event) => {
    const files = Array.from(event.target.files);
    
    if (photos.length + files.length > 10) {
      setError('Максимальное количество фотографий - 10');
      return;
    }

    // Process files one by one to ensure they're all handled
    for (const file of files) {
      try {
        // Create object URL for preview
        const objectUrl = URL.createObjectURL(file);
        
        // Verify the file loaded correctly
        await new Promise((resolve, reject) => {
          const img = new Image();
          img.onload = () => resolve();
          img.onerror = () => reject();
          img.src = objectUrl;
        });

        setPhotos(prevPhotos => [...prevPhotos, objectUrl]);
      } catch (err) {
        console.error('Error loading photo:', err);
        setError('Ошибка при загрузке фотографии. Пожалуйста, попробуйте другое изображение.');
      }
    }
  };

  const removePhoto = (index) => {
    setPhotos(prevPhotos => {
      const newPhotos = [...prevPhotos];
      URL.revokeObjectURL(newPhotos[index]); // Clean up object URL
      newPhotos.splice(index, 1);
      return newPhotos;
    });
  };

  const ConfirmationPopup = ({ onConfirm, onCancel }) => (
    <div className="confirmation-popup">
      <p>Вы уверены что хотите отправить отзыв без текста?</p>
      <div className="confirmation-buttons">
        <button onClick={onConfirm}>Да</button>
        <button onClick={onCancel}>Нет</button>
      </div>
    </div>
  );

  useEffect(() => {
    const setupMainButton = () => {
      tg.MainButton.setParams({
        text: isSubmitting ? 'Отправка...' : 'Отправить',
        color: '#4CAF50',
        disable: isSubmitting
      });
      tg.MainButton.onClick(handleSubmit);
      tg.MainButton.show();
    };

    setupMainButton();

    return () => {
      tg.MainButton.offClick(handleSubmit);
      tg.MainButton.hide();
    };
  }, [tg.MainButton, handleSubmit, isSubmitting]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const fetchedOrder = await getOneOrder(id, tg.initData);
        setOrder(fetchedOrder);
        if (fetchedOrder && fetchedOrder.product_id) {
          const fetchedProduct = await getOneProduct(fetchedOrder.product_id);
          setProduct(fetchedProduct);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        setError('Произошла ошибка при загрузке данных.');
      }
    };
    fetchData();
  }, [id, tg.initData]);

  if (!product || !order) return (
    <div className="loading-container">
      <CircularProgress />
    </div>
  );

  return (
    <div className="post-feedback-container">
      <h2 className="feedback-title">Оставить отзыв</h2>
      <div className="product-info">
        <img src={product.image_url} alt={product.name} className="product-image" />
        <div className="product-details">
          <p className="product-name">{product.name}</p>
          <p className="product-price">{order.price} ₽</p>
        </div>
      </div>
      {error && <p className="error-message">{error}</p>}
      <div className="feedback-form">
        <div className="rating-container">
          <p className="rating-label">Рейтинг</p>
          <div className="star-rating">
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                type="button"
                className={`star-button ${star <= rating ? 'active' : ''}`}
                onClick={() => setRating(star)}
              >
                ★
              </button>
            ))}
          </div>
        </div>
        <div className="review-container">
          <label htmlFor="review" className="review-label">Текст отзыва</label>
          <textarea
            id="review"
            className={`review-textarea ${error ? 'error' : ''}`}
            placeholder="Введите текст..."
            value={review}
            onChange={(e) => {
              setReview(e.target.value);
              if (error) setError('');
              tg.MainButton.show();
            }}
            onFocus={() => tg.MainButton.hide()}
            onBlur={() => tg.MainButton.show()}
            maxLength={500}
          ></textarea>
          <p className="character-count">{review.length}/500 символов</p>
          <div className="photo-upload">
              <button 
                className="photo-upload-button"
                onClick={() => {
                  const input = document.createElement('input');
                  input.type = 'file';
                  input.accept = 'image/*';
                  input.multiple = true;
                  input.onchange = handlePhotoUpload;
                  input.click();
                }}
              >
                Прикрепить фото (макс. 10)
              </button>
          </div>
          <div className="photo-preview">
            {photos.map((photo, index) => (
              <div key={index} className="photo-item">
                <img src={photo} alt={`Фото ${index + 1}`} style={{ width: '50px', height: '50px', objectFit: 'cover' }} />
                <button onClick={() => removePhoto(index)}>Удалить</button>
              </div>
            ))}
          </div>
        </div>
      </div>
      {showConfirmation && (
        <ConfirmationPopup
          onConfirm={() => {
          setShowConfirmation(false);
          submitReview();
        }}
        onCancel={() => setShowConfirmation(false)}
        />
      )}
    </div>
  );
};

export default PostFeedback;