import React from 'react';
import '../styles/components/ProfburoMemberCard.css'
const ProfburoMemberCard = ({member}) => {
    return (
        <div className="profburoMemberCard">
            <div className="member__role">{member.direction}</div>
            <img src={member.photo} alt="member-photo"/>
            <div className="member__fio">
                <div>{member.firstname}</div>
                <div>{member.surname}</div>
            </div>
        </div>
    );
};

export default ProfburoMemberCard;