import React, {useEffect, useState} from 'react';
import Button from "../../Components/Button";
import arrowGreater from '../../images/arrow_greater.png';
import TabScreen from "../../Components/TabScreen/TabScreen";
import {useNavigate} from "react-router-dom";
import {useTelegram} from '../../hooks/useTelegram';
import {getUser} from '../../db/db';
import CircularProgress from '@mui/material/CircularProgress';
import profilePhoto from '../../images/feedback_photo.PNG';
import './Profile.css';

function Profile() {
    const navigate = useNavigate();
    const {tg, user} = useTelegram();
    const [db_user, setDbUser] = useState(null);
    const [loading, setLoading] = useState(true);

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
        async function fetchUser() {
            try {
                const userData = await getUser(tg.initData);
                setDbUser(userData);
            } catch (error) {
                console.error("Error fetching user data:", error);
            } finally {
                setLoading(false);
            }
        }
        fetchUser();
    }, [tg]);

    if (loading || !db_user) {
        return (
            <div className="loading-container">
                <CircularProgress />
            </div>
        );
    }

    return <div>
        <div className="profile-header">
            <h3>Профиль</h3>
        </div>
        <div className="profile-user-info">
            <div className="profile-avatar-container">
                <img 
                    className="profile-avatar"
                    src={user.photo_url} 
                    onError={(e) => {
                        e.target.onerror = null;
                        e.target.src = profilePhoto;
                    }}
                    alt="Profile"
                />
            </div>
            <div className="profile-user-details">
                <b>{user?.first_name} {user?.last_name}</b>
                <span className="profile-username">@{user?.username}</span>
            </div>
        </div>
        <div className="profile-balance">
            <h3>Баланс: {parseFloat(db_user.balance).toLocaleString('ru-RU', {maximumFractionDigits: 2})} ₽</h3>
            <span className="profile-deposit-link" onClick={() => navigate('/deposit')}>Пополнить</span>
        </div>

        <div className="profile-buttons">
            <Button onClick={() => {navigate('/my-referral')}} className="px-08" type='info' image={arrowGreater} image_invert={true} title='Реферальная система'></Button>
            <Button onClick={() => {navigate('/promo-code')}} className="px-08" type='info' image={arrowGreater} image_invert={true} title='Ввести промокод'></Button>
        </div>

        <TabScreen/>
    </div>
}

export default Profile;