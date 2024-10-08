import React, {useContext} from 'react';
import './myNavbar.css';
import MyAuthButton from "../buttons/MyAuthButton/myAuthButton";
import {useLocation, useNavigate} from "react-router-dom";
import {AuthContext} from "../../../context";
import {scrollToElement} from "../../../utils";
const MyNavbar = () => {

    let location = useLocation();
    const navigate = useNavigate();

    let isElementsHidden = location.pathname !== '/'


    const {isAuth, setIsAuth} = useContext(AuthContext)

    const unlogin = (event) => {
        event.preventDefault();
        setIsAuth(false);
        localStorage.removeItem('access_token');
    };

    const login = () => {
        navigate('/login')
    }


    return (
        <header id='start' className='myNavbar' style={isElementsHidden ? {justifyContent: 'center'} : {} }>
            <img src='/images/logo_without_bg.svg' onClick={() => navigate('/')} alt="logo"/>
            {isElementsHidden ? null : <ul>
                <li>Главная</li>
                <li onClick={() => scrollToElement('faq')}>FAQ</li>
                {/*{isAuth ? <li onClick={() => scrollToElement('support')}>Поддержка</li> : null}*/}
            </ul>}
            {isElementsHidden ? null : isAuth ? <MyAuthButton isAuth={true} onClick={unlogin}>Выйти</MyAuthButton> : <MyAuthButton onClick={login}>Войти</MyAuthButton> }
        </header>
    );
};

export default MyNavbar;