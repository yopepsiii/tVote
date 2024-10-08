import React, {useContext, useEffect, useRef, useState} from 'react';
import '../styles/Block1.css'
import '../styles/Block2.css'
import '../styles/Block3.css'
import '../styles/Block4.css'
import '../styles/Block5.css'
import MyButton from "../components/UI/buttons/MyButton/myButton";
import CandidateCardList from "../components/CandidateCardList";
import ProfburoMemberCardList from "../components/ProfburoMemberCardList";
import MyFooter from "../components/UI/footer/MyFooter";
import {AuthContext} from "../context";
import {scrollToElement} from "../utils";
import MyVoteButton from "../components/UI/buttons/myVoteButton/myVoteButton";
import {useLoading} from "../hooks/useLoading";
import {CandidatesService} from "../API/CandidatesService";
import {useObserver} from "../hooks/useObserver";
import {UsersService} from "../API/UsersService";
import FAQList from "../components/FAQList";
import {Toaster} from "react-hot-toast";
import Loader from "../components/UI/Loader/Loader";
import ErrorBanner from "../components/UI/ErrorBanner/ErrorBanner";

const IndexPage = () => {


    const {isAuth} = useContext(AuthContext)

    const candidatesBlockStart = useRef()
    const profburoBlockStart = useRef()

    const [toLoadMarkers, setToLoadMarkers] = useState({
        // нужно ли загружать информацию из API или нет
        'candidatesBlock' : true,
        'profburoBlock' : true,
    })

    const [candidates, setCandidates] = useState([])
    const [profburoMembers, setProfburoMembers] = useState([])

    const [fetchCandidates, isCandidatesLoading, candidatesError] = useLoading(async () => {
        const res = await CandidatesService.getCandidates()
        setCandidates([...res])
    });
    const [fetchProfburoMembers, isProfburoMembersLoading, profburoMembersError] = useLoading(async () => {
        const res = await CandidatesService.getProfburoMembers()
        setProfburoMembers([...res])
    });


    const [currentProfburoVoteType, setcurrentProfburoVoteType] = useState(null);

    useObserver(candidatesBlockStart, toLoadMarkers['candidatesBlock'], isCandidatesLoading, async () => {
        await fetchCandidates()
        let updated = toLoadMarkers
        updated['candidatesBlock'] = false
        setToLoadMarkers(updated)
    })

    useObserver(profburoBlockStart, toLoadMarkers['profburoBlock'], isProfburoMembersLoading, async () => {
        await fetchProfburoMembers()
        let updated = toLoadMarkers
        updated['profburoBlock'] = false
        setToLoadMarkers(updated)
    })

    const [userVotes, setUserVotes] = useState([]);
    const [fetchUserVotes, isUserVotesLoading, userVotesError] = useLoading(async () => {
        const res = await UsersService.getMe()
        setUserVotes([...res.votes])
        setcurrentProfburoVoteType(res.profburo_vote.type)
    });

    useEffect(() => {
        if (localStorage.getItem('access_token')) {
            fetchUserVotes()
        }

    }, []);






    return (
        <div className='index-page'>
            <section className="welcome-block">
                <div className="left-block">
                    <div className="left-block__title">Вы решаете каким будет будущее</div>
                    <div className="left-block__subtitle">На этих выборах решится кто будет следующим председателем профсоюза Т-Университета.</div>
                    <MyButton style={{color: '#00303D', }}
                              onClick={() => scrollToElement('candidates')}>Голосовать</MyButton>
                </div>
                <div className="right-block">
                    <img src="/images/right_part.png" alt="img"/>
                </div>
                <img className='welcome-block__bg' src="/images/bg_block1.svg" alt="bg"/>
            </section>
            <section ref={candidatesBlockStart} id='candidates'  className="candidates-block">
                {isCandidatesLoading ? <Loader/> : <CandidateCardList toLoadMarkers={toLoadMarkers} userVotes={userVotes} setUserVotes={setUserVotes} setCandidates={setCandidates} candidates={candidates}/>}
                {candidatesError ? <ErrorBanner errorText={candidatesError}/> : null}
            </section>
            <section ref={profburoBlockStart} className="block">
                <div className="head">
                    <div className="head__title">Согласны ли вы с таким составом профбюро?</div>
                    <div className="head__subtitle">Ваш голос решит их дальнейшую судьбу.
                        Голосуйте.</div>
                </div>
                <div className="profburo__members">
                    {isProfburoMembersLoading ? <Loader/> : <ProfburoMemberCardList members={profburoMembers}/>}
                    {profburoMembersError ? <ErrorBanner errorText={profburoMembersError}/> : null}
                </div>
                <div className="profburo__buttons">
                    <MyVoteButton isAuth={isAuth} setCurrentType={setcurrentProfburoVoteType} buttonType={1} candidateId={'profburo'} isActive={currentProfburoVoteType === 1}></MyVoteButton>
                    <MyVoteButton isAuth={isAuth} setCurrentType={setcurrentProfburoVoteType} buttonType={0} candidateId={'profburo'} isActive={currentProfburoVoteType === 0}></MyVoteButton>
                    <MyVoteButton isAuth={isAuth} setCurrentType={setcurrentProfburoVoteType} buttonType={2} candidateId={'profburo'} isActive={currentProfburoVoteType === 2}></MyVoteButton>
                </div>
            </section>
            <section id='faq' className="block">
                <div className="head">
                    <div className="head__title">FAQ</div>
                    <div className="head__subtitle">Тут вы сможете найти ответы на самые часто задаваемые вопросы.</div>
                </div>
                <FAQList/>
            </section>
            {/*{isAuth ? <section id='support' className='block'>*/}
            {/*    <div className="head">*/}
            {/*        <div className="head__title">Поддержка</div>*/}
            {/*        <div className="head__subtitle">Нашли ошибку? Или текст не соответствует действительности? Напиши*/}
            {/*            сюда, тут помогут.*/}
            {/*        </div>*/}
            {/*    </div>*/}
            {/*    <MyTextArea/>*/}
            {/*    <MyButton style={{color: '#fff', padding: '15px 100px', borderRadius: 15}}>Отправить</MyButton>*/}
            {/*</section> : <div id='support' className='block'/>}*/}
            <MyFooter/>

        </div>
    );
};

export default IndexPage;