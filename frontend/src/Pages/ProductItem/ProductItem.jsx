import React, {useState, useEffect} from 'react';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { getOneProduct, getUser } from '../../db/db';
import { useTelegram } from '../../hooks/useTelegram';
import CircularProgress from '@mui/material/CircularProgress';

function ProductItem() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [product, setProduct] = useState(null);
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const { tg } = useTelegram();

    const handlePurchase = () => {
        if (user && product) {
            let balance = parseFloat(user.balance);
            let price = parseFloat(product.price);
    
            if (balance >= price) {
                navigate(`/product/checkout/${id}`);
            } else {
                navigate(`/deficiency/${id}`);
            }
        } else {
            console.log('User or product is null');
        }
    };
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
        const fetchProduct = async () => {
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
            const user = await getUser(tg.initData);
            setUser(user);
        }
        fetchUser();
    }, []);

    useEffect(() => {
        tg.MainButton.setText('Купить');
        tg.MainButton.show();
        tg.MainButton.onClick(handlePurchase);

        return () => {
            tg.MainButton.offClick(handlePurchase);
            tg.MainButton.hide();
        };
    }, [user, product, id]);

    const renderDescription = (text) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.split('\n').map((paragraph, paragraphIndex) => (
            <p key={paragraphIndex}>
                {paragraph.split(urlRegex).map((part, partIndex) => 
                    urlRegex.test(part) ? (
                        <a key={partIndex} href={part} target="_blank" rel="noopener noreferrer">{part}</a>
                ) : (
                        part
                    )
                )}
            </p>
            ));
        };

    if (loading) {
        return (
            <div className="flex justify-center align-items-center" style={{height: '100vh'}}>
                <CircularProgress />
            </div>
        );
    }

    return (
        <div style={{height: "100vh", display: "flex", flexDirection: "column"}} className='relative'>
            <div className="flex-grow overflow-auto">
                <div className="">
                    <img className='card__image rounded-1' src={product.image_url} alt={product.name} style={{maxHeight: "90vh", objectFit: "cover", width: "100%"}}/>
                </div>
                <div className="flex column justify-between px-08 py-04">
                    <div className="flex justify-between">
                        <b>
                            {product.name}
                        </b>
                        <b>{product.price} ₽</b>
                    </div>
                    <div className="flex py-04">
                        <h3>Описание</h3>
                    </div>
                    <div className="bg-lightgray rounded px-08 py-08" style={{overflowWrap: 'break-word', wordBreak: 'break-word'}}>
                        <div className="description-text">
                            {renderDescription(product.description)}
                        </div>
                    </div>
                    <style>
                        {`
                        .description-text p {
                            margin-bottom: 0.5rem;
                        }
                        .description-text p:last-child {
                            margin-bottom: 0;
                        }
                        `}
                    </style>
                </div>
            </div>
        </div>
    );
}

export default ProductItem;