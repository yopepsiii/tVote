import React, { useState } from "react";
import './myInput.css';

const MyInput = ({isPasswordInput, imgSrc, placeholder, onChange}) => {
    const [passwordVisible, setPasswordVisible] = useState(false);


    const togglePasswordVisibility = () => {
        setPasswordVisible(!passwordVisible);
    };

    return (
        <div className="myInput">
            <img src={imgSrc} alt="icon"/>
            <input
                type={isPasswordInput ? passwordVisible ? "text" : "password" : 'text'}
                placeholder={placeholder}
                className="input"
                onChange={onChange}
            />
            {isPasswordInput ? <button
                type="button"
                className="toggle-button"
                onClick={togglePasswordVisibility}
            >
                {passwordVisible ? "Скрыть" : "Показать"}
            </button> : null}

        </div>
    );
};

export default MyInput;
