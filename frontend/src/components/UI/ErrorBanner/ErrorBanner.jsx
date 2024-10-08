import React from 'react';
import cl from './ErrorBanner.module.css'
const ErrorBanner = ({errorText, props}) => {
    return (
        <div className={cl.errorBanner}>
            <div className={cl.errorBanner__title}>Ошибка!</div>
            <div className={cl.errorBanner__description}>{errorText}</div>
        </div>
    );
};

export default ErrorBanner;