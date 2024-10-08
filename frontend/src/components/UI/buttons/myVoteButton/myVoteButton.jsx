import React from 'react';
import './myVoteButton.css';
import { VoteService } from '../../../../API/VoteService';
import {useNavigate} from "react-router-dom";
import toast from "react-hot-toast";

const MyVoteButton = ({
                          isAuth,
                          isActive,
                          candidateId,
                          children,
                          buttonType,
                          setUserVotes,
                          userVotes,
                          candidatesVotes,
                          setCandidatesVotes,
                          setCurrentType
                      }) => {
    let className = 'myVoteButton__';
    let voteCountType = '';
    let svgSource = '';
    const navigate = useNavigate();

    switch (buttonType) {
        case 0:
            className += 'dislike';
            voteCountType = 'dislikes_count';
            svgSource = '/images/Dislike.svg'
            break;
        case 1:
            className += 'like';
            voteCountType = 'likes_count';
            svgSource = '/images/Like.svg'
            break;
        case 2:
            className += 'abstain';
            voteCountType = 'abstaines_count';
            svgSource = '/images/Abstain.svg'
            break;
        default:
            break;
    }

    if (isActive) {
        className += '__pressed';
        switch (buttonType) {
            case 0:
                svgSource = '/images/Dislike_filled.svg'
                break
            case 1:
                svgSource = '/images/Like_filled.svg'
                break
            case 2:
                svgSource = '/images/Abstain_filled.svg'
        }
    }

    const handleVoteClick = async () => {
        let newVotes = [...userVotes];
        let newCandidatesVotes = [...candidatesVotes];
        let currentCandidateVotes = newCandidatesVotes.find(obj => obj.candidate_id === candidateId);

        if (!currentCandidateVotes) return;

        if (isActive) {
            // Если кнопка активна, снимаем текущий голос
            newVotes = newVotes.filter(vote => vote.candidate_id !== candidateId);
            currentCandidateVotes[voteCountType]--;
        } else {
            // Снимаем голос других типов у того же кандидата
            const existingVote = newVotes.find(vote => vote.candidate_id === candidateId);
            if (existingVote) {
                // Уменьшаем счетчики других типов голосов
                if (existingVote.type === 1) currentCandidateVotes['likes_count']--;
                if (existingVote.type === 2) currentCandidateVotes['abstaines_count']--;
                if (existingVote.type === 0) currentCandidateVotes['dislikes_count']--;

                // Обновляем тип голоса
                existingVote.type = buttonType;
            } else {
                // Если голосов нет, добавляем новый
                newVotes.push({ candidate_id: candidateId, type: buttonType });
            }

            // Увеличиваем счетчик нового типа голоса
            currentCandidateVotes[voteCountType]++;

            // Если это "лайк", снимаем голос "за" с других кандидатов
            if (buttonType === 1) {
                const likedCandidate = newVotes.find(vote => vote.type === 1 && vote.candidate_id !== candidateId);
                if (likedCandidate) {
                    let likedCandidateVotes = newCandidatesVotes.find(obj => obj.candidate_id === likedCandidate.candidate_id);
                    if (likedCandidateVotes) {
                        likedCandidateVotes['likes_count']--;
                    }
                    newVotes = newVotes.filter(vote => vote.candidate_id !== likedCandidate.candidate_id);
                }
            }
        }
        setCandidatesVotes(newCandidatesVotes);
        setUserVotes(newVotes);
        try {
            const res = await VoteService.voteToCandidate(candidateId, buttonType);
        }
        catch (e) {
            if (e.response.status === 401) {
                toast.error('Ошибка авторизации, перезайдите в аккаунт')
            }
            else {
                toast.error(e.message)
            }

        }



    };

    const handleProfburoVote = async () => {
        setCurrentType(isActive ? null : buttonType);
        try {
            const res = await VoteService.voteToProfburo(buttonType);
        }
        catch (e) {
            if (e.response.status === 401) {
                toast.error('Ошибка авторизации, перезагрузите страницу')
            }
            else {
                toast.error(e.message)
            }

        }

    };

    const redirectToLogin = () => {
        navigate('/login')
    }

    return (
        <button
            onClick={isAuth ? candidateId === 'profburo' ? handleProfburoVote : handleVoteClick : redirectToLogin}
            className={className}
        >
            {children}
            <img className='myVoteButton__icon' src={svgSource} alt="hand"/>
        </button>
    );
};

export default MyVoteButton;