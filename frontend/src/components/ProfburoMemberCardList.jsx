import React from 'react';
import ProfburoMemberCard from "./ProfburoMemberCard";
import '../styles/components/ProfburoMemberCardList.css'

const ProfburoMemberCardList = ({members}) => {
    return (
        <div className="profburoMemberCardList">
            {members.map(member => (
                <ProfburoMemberCard key={member.id} member={member} />
            ))}
        </div>
    );
};

export default ProfburoMemberCardList;