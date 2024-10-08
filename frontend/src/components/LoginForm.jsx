import React, {useContext, useState} from 'react';
import '../styles/components/LoginForm.css'
import MyInput from "./UI/input/MyInput";
import MyButton from "./UI/buttons/MyButton/myButton";
import AuthService from "../API/AuthService";
import {useNavigate} from "react-router-dom";
import {AuthContext} from "../context";
import {useLoading} from "../hooks/useLoading";
import Loader from "./UI/Loader/Loader";
import ErrorBanner from "./UI/ErrorBanner/ErrorBanner";

const LoginForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const {isAuth, setIsAuth} = useContext(AuthContext);

    const navigate = useNavigate();

    const [loginFunc, isLoading, loginError] = useLoading(async() => {
        const res = await AuthService.Login(email, password)
        if (res) {
            setIsAuth(true)
            return navigate('/')
        }

    })


    return (
        <div className="Login-container">
            <div className='loginForm'>
                <div className="loginForm__headInfo ">
                    <div className="headInfo__title">Вход</div>
                    <div className="headInfo__subtitle">Войдите, чтобы голосовать</div>
                </div>
                <div className="loginForm__inputs">
                    <MyInput imgSrc={'/images/Mail.svg'} onChange={e => setEmail(e.target.value)} placeholder='Почта'/>
                    <MyInput isPasswordInput={true} imgSrc={'/images/Key.svg'}
                             onChange={e => setPassword(e.target.value)} placeholder='Пароль'/>
                </div>
                {isLoading ? <Loader/> : <MyButton
                    style={{color: '#fff', padding: '13px 25px', borderRadius: 15}}
                    onClick={loginFunc}>Войти</MyButton>}

            </div>
        </div>

    );
};

export default LoginForm;