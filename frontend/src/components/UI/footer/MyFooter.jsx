import React, {useContext} from 'react';
import './MyFooter.css'
import {scrollToElement} from "../../../utils";
import {AuthContext} from "../../../context";
const MyFooter = () => {
    const {isAuth} = useContext(AuthContext);
    return (
        <footer className="footer">
            <div className="footer__info">
                <div className="info__links">
                    <div onClick={() => scrollToElement('start')}>Главная
                        <img src="/images/Home.svg" alt="home"/>
                    </div>
                    <div onClick={() => scrollToElement('candidates')}>Голосование
                        <img src="/images/Elections.svg" alt="elections"/>
                    </div>
                    {/*{isAuth ? null : <div onClick={() => scrollToElement('faq')}>FAQ*/}
                    {/*    <img src="/images/Question%20Mark.svg" alt="faq"/>*/}
                    {/*</div>}*/}
                </div>
                <div className="info__socials">
                    <a href='https://vk.com/t.donstu'>
                    <img src="/images/VK%20Circled.svg" alt="tdonstu_vk"/>
                        t.donstu
                    </a>
                    <a href='https://vk.com/prof_t_university'>
                        <img src="/images/VK%20Circled.svg" alt="prof_vk"/>
                        prof.t
                    </a>
                    <a href='https://t.me/profdstu'>
                        <img src="/images/Telegram.svg" alt="prof_tg"/>
                        profdstu
                    </a>
                </div>
            </div>
            <img className='footer__line' src="/images/underline.svg" alt="underline"/>
            <div className="info__developers">
                Остались вопросы?
                <a href='https://t.me/oshinogj'>
                    <img src="/images/Laptop.svg" alt="laptop"/>
                    @oshinogj
                </a>
            </div>
        </footer>
    );
};

export default MyFooter;