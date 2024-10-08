import React from 'react';
import MyFooter from "../../components/UI/footer/MyFooter";
import '../../styles/NoMatchPage.css'

const NoMatch = () => {
    return (
        <section className="noMatch">
            <div className="noMatch__title">404</div>
            <div className="noMatch__description">Увы, тут ничего нет.</div>
        </section>
    );
};

export default NoMatch;