import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';
import { getOneOrder, getOneProduct, getOneCategory } from '../../db/db';
import { useNavigate } from 'react-router-dom';
import { useTelegram } from '../../hooks/useTelegram';
import CircularProgress from '@mui/material/CircularProgress';

function OrderDetails() {
    const navigate = useNavigate();
    const [order, setOrder] = useState(null);
    const [product, setProduct] = useState(null);
    const [category, setCategory] = useState(null);
    const [loading, setLoading] = useState(true);
    const {id} = useParams();
    const { tg } = useTelegram();
 
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
        const fetchData = async () => {
            const orderData = await getOneOrder(id, tg.initData);
            const productData = await getOneProduct(orderData.product_id);
            const categoryData = await getOneCategory(productData.category_id);
            setOrder(orderData);
            setProduct(productData);
            setCategory(categoryData);
            setLoading(false);
        }
        fetchData();
    }, [id]);

    const handleLeaveFeedback = () => {
        navigate(`/post-feedback/${order.id}`);
    };

    useEffect(() => {
        if (order && order.status === "COMPLETED") {
            tg.MainButton.setText("Оставить отзыв");
            tg.MainButton.show();
            tg.MainButton.onClick(handleLeaveFeedback);
        } else {
            tg.MainButton.hide();
        }

        return () => {
            tg.MainButton.offClick();
            tg.MainButton.hide();
        };
    }, [order, product]);

    const renderAdditionalFields = () => {
        if (!order || !order.additional_data) return null;
    
        const additionalData = order.additional_data;

        return Object.entries(additionalData).map(([key, value]) => (
            <div className="detail-item" key={key}>
                <div className="label">{key.charAt(0).toUpperCase() + key.slice(1)}</div>
                <div className="value">{value}</div>
            </div>
        ));
    };
    
    return (
        <div className="transaction-detail">
            <h2 className="text-2xl font-bold mb-4">Информация о заказе</h2>
            {loading ? (
                <div className="flex justify-center align-items-center" style={{height: '100vh'}}>
                    <CircularProgress />
                </div>
            ) : (
                <>
                    <div className="detail-item">
                        <div className="label">ID заказа</div>
                        <div className="value">{order.id}</div>
                    </div>
                    
                    <div className="detail-item">
                        <div className="label">Дата и время заказа</div>
                        <div className="value">
                            {new Date(order.time).toLocaleString('ru-RU', { 
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
                        <div className="label">Товар</div>
                        <div className="value">{product.name}</div>
                    </div>

                    <div className="detail-item">
                        <div className="label">ID товара</div>
                        <div className="value">{product.id}</div>
                    </div>

                    <div className="detail-item">
                        <div className="label">Стоимость</div>
                        <div className="value">{order.price}</div>
                    </div>
    
                    <div className="detail-item">
                        <div className="label">Статус заказа</div>
                        <div className="value">
                            {order.status === "PAID" ? "Оплачено" : 
                            order.status === "CLOSED" ? "Закрыт" :
                            order.status === "COMPLETED" ? "Выполнен" :
                            order.status === "PROGRESS" ? "В обработке" :
                            null}
                        </div>
                    </div>
    
                    {renderAdditionalFields()}
                </>
            )}
        </div>
    );
}

export default OrderDetails;