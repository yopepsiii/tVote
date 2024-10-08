import React from 'react';
import FAQItem from './FAQItem';  // Импортируем наш компонент FAQItem
import '../styles/components/FAQList.css'

const FAQList = () => {
    const faqs = [
        { question: 'Как проголосвать за кандидата', answer: 'Сначала необходимо войти в свой аккаунт. Пароль должен быть у вас на почте, но если он не пришел, то напишите главному разработчику. После успешного входа станет доступно голосование.' },
        { question: 'Как голосовать то?', answer: 'Тыкаешь такой на вход сначала и потоом на кнопки голоса.' },
        { question: 'Как голосовать то?', answer: 'Тыкаешь такой на вход сначала и потоом на кнопки голоса.' }
    ];

    return (
        <div className="faq-list">
            {faqs.map((faq, index) => (
                <FAQItem key={index} question={faq.question} answer={faq.answer} />
            ))}
        </div>
    );
};

export default FAQList;
