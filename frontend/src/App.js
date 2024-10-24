import './App.css';
import React from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
} from "react-router-dom";
import { useEffect } from 'react';
import { WebAppProvider } from '@vkruglikov/react-telegram-web-app';
import Main from "./Pages/Main/Main";
import Profile from "./Pages/Profile/Profile";
import OrderDetails from "./Pages/OrderDetails/OrderDetails";
import PromoCode from "./Pages/PromoCode/PromoCode";
import MyReferral from "./Pages/MyReferral/MyReferral";
import Deposit from "./Pages/Deposit/Deposit";
import Products from "./Pages/Products/Products";
import ProductItem from "./Pages/ProductItem/ProductItem";
import TransactionDetail from "./Pages/TransactionDetail/TransactionDetail";
import {SearchProducts} from "./Pages/SearchProducts/SearchProducts";
import PaymentProcessing from "./Pages/PaymentProcessing/PaymentProcessing";
import Feedbacks from "./Pages/Feedbacks/Feedbacks";
import PostFeedback from "./Pages/PostFeedback/PostFeedback";
import DeficiencyDeposit from './Pages/DeficiencyDeposit/DeficiencyDeposit';
import OrderProcessing from './Pages/OrderProcessing/OrderProcessing';
import OrderCreated from './Pages/OrderCreated/OrderCreated';
import { SearchPage } from './Pages/Search/Search';
import { useTelegram } from './hooks/useTelegram';
import Category from './Pages/Category/Category';

function App() {
    const { expand } = useTelegram();

    useEffect(() => {
        expand();
    }, [expand]);

    return (
        <WebAppProvider>
            <Router>
                <Routes>
                    <Route exact path="/search" element={<SearchProducts/>}/>
                    <Route exact path="/" element={<Main/>}/>
                    <Route exact path="/profile" element={<Profile/>}/>
                    <Route exact path="/orders/:id" element={<OrderDetails/>}/>
                    <Route exact path="/deposit" element={<Deposit/>}/>
                    <Route exact path="/my-referral" element={<MyReferral/>}/>
                    <Route exact path="/promo-code" element={<PromoCode/>}/>
                    <Route exact path="/game" element={<Category/>}/>
                    <Route exact path="/category" element={<Products/>}/>
                    <Route exact path="/product/:id/" element={<ProductItem/>}/>
                    <Route exact path="/transactions" element={<TransactionDetail/>}/>
                    <Route exact path="/payment/:order_id" element={<PaymentProcessing/>}/>
                    <Route exact path="/feedbacks" element={<Feedbacks/>}/>
                    <Route exact path="/post-feedback/:id" element={<PostFeedback/>}/>
                    <Route exact path="/deficiency/:id" element={<DeficiencyDeposit/>}/>
                    <Route exact path="/product/checkout/:id" element={<OrderProcessing/>}/>
                    <Route exact path="/order/success" element={<OrderCreated/>}/>
                    <Route path="/search" element={<SearchPage />} />
                    <Route path="*" element={<Main/>}/>
                </Routes>
            </Router>
        </WebAppProvider>
    );
}

export default App;