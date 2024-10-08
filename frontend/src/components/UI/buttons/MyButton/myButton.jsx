import React from 'react';
import cl from './myButton.module.css'

const MyButton = ({props, children, onClick, style}) => {
    return (
        <button {...props} onClick={onClick} style={style} className={cl.myBtn}>
            {children}
        </button>
    );
};

export default MyButton;