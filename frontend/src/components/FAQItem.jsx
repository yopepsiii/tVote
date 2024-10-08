import React, { useState } from 'react';
import '../styles/components/FAQItem.css'

const FAQItem = ({ question, answer }) => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleOpen = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div className="faq-item">
            <div className="faq-question" onClick={toggleOpen}>
                <p>{question}</p>
                <img className={isOpen ? "faq-toggle__flipped" : "faq-toggle"} src="/images/Expand%20Arrow.svg" alt="faq_arrow"/>
            </div>
            <div className={isOpen ? 'faq-answer' : 'faq-answer__hidden'}>
                <p>{answer}</p>
            </div>
            <img src="/images/faq_line.svg" alt="faq_line"/>
        </div>
    );
};

export default FAQItem;
