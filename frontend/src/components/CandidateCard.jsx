import React, {useContext, useEffect, useState} from 'react';
import '../styles/components/CandidateCard.css'
import MyVoteButton from "./UI/buttons/myVoteButton/myVoteButton";
import {AuthContext} from "../context";



const CandidateCard = ({candidate, position, candidatesVotes, setCandidatesVotes, userVotes, setUserVotes, isLiked}) => {

    const [currentType, setCurrentType] = useState(null);
    const [currentCandidateVotes, setCurrentCandidateVotes] = useState({});
    const {isAuth} = useContext(AuthContext)


    useEffect(() => {
        const findedVote = userVotes.find(vote => vote.candidate_id === candidate.id)
        if (findedVote) {
            setCurrentType(findedVote.type)
        } else {
            setCurrentType(null)
        }

    }, [userVotes]);

    useEffect(() => {
        if (candidatesVotes.length > 0) {
            const fetchedCurrentVotes = candidatesVotes.find(obj => obj.candidate_id === candidate.id)
            setCurrentCandidateVotes(fetchedCurrentVotes)
        }
    }, [candidatesVotes]);



    return (
        <div className='candidate-card'>
            <img src={candidate.photo} alt="candidate-photo"/>
            <div className="candidate__info-block">
                <div className="info-block__main_info">
                    <div className="main_info__position">#{position}</div>
                    <div className="main_info__fio">
                        <div>{candidate.firstname}</div>
                        <div>{candidate.surname}</div>
                    </div>
                </div>
                <div className="info-block__additional_info">
                    <div className="additional_info__text">{candidate.year_of_study} курс</div>
                    <div className="additional_info__text">{candidate.group}</div>
                    <div className="additional_info__text">{candidate.study_dirrection}</div>
                </div>
                <div className="info_block__buttons">
                    <MyVoteButton isAuth={isAuth} setCandidatesVotes={setCandidatesVotes} candidatesVotes={candidatesVotes} userVotes={userVotes} setUserVotes={setUserVotes} buttonType={1} candidateId={candidate.id} isActive={isLiked}>{currentCandidateVotes.likes_count}</MyVoteButton>
                    <MyVoteButton isAuth={isAuth} setCandidatesVotes={setCandidatesVotes} candidatesVotes={candidatesVotes} userVotes={userVotes} setUserVotes={setUserVotes} buttonType={0} candidateId={candidate.id} isActive={currentType === 0}>{currentCandidateVotes.dislikes_count}</MyVoteButton>
                    <MyVoteButton isAuth={isAuth} setCandidatesVotes={setCandidatesVotes} candidatesVotes={candidatesVotes} userVotes={userVotes} setUserVotes={setUserVotes} buttonType={2} candidateId={candidate.id} isActive={currentType === 2}>{currentCandidateVotes.abstaines_count}</MyVoteButton>
                </div>

            </div>
        </div>
    );
};

export default CandidateCard;