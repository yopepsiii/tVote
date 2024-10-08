import React from 'react';
import cl from './myAuthButton.module.css'
const MyAuthButton = ({children, onClick, isHidden, isAuth}) => {

    return (
        <div onClick={onClick} className={isHidden ? cl.myAuthButton__hidden : isAuth ? cl.myAuthButton__active : cl.myAuthButton}>
            {children}
        </div>
    );
};

export default MyAuthButton;