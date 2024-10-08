import React, {useEffect, useState} from 'react';
import CandidateCard from "./CandidateCard";
import '../styles/components/CandidateCardList.css'

const CandidateCardList = ({candidates, userVotes, setUserVotes}) => {

    const [likedCandidate, setLikedCandidate] = useState(null);
    const [candidatesVotes, setCandidatesVotes] = useState([]);


    useEffect(() => {
        const vote = userVotes.find(vote => vote.type === 1); // Ищем лайк (type === 1)
        if (vote) {
            setLikedCandidate(vote.candidate_id);
        } else {
            setLikedCandidate(null);
        }
    }, [userVotes]);

    useEffect(() => {
        if (candidates.length > 0) {
            const fetchedCandidatesVotes = candidates.map((candidate) => (
                {
                    'candidate_id': candidate.id,
                    'likes_count': candidate.likes_count,
                    'dislikes_count': candidate.dislikes_count,
                    'abstaines_count': candidate.abstaines_count,
                }
            ));
            setCandidatesVotes(fetchedCandidatesVotes);
        }
    }, [candidates]);




    return (
        <div className='candidateCardList'>
            {candidates.map((candidate, index) => (
                <CandidateCard
                    isLiked={candidate.id === likedCandidate}
                    userVotes={userVotes}
                    setUserVotes={setUserVotes}
                    candidatesVotes={candidatesVotes}
                    setCandidatesVotes={setCandidatesVotes}
                    key={candidate.id}
                    candidate={candidate}
                    position={index + 1}
                />
            ))}
        </div>
    );
};

export default CandidateCardList;