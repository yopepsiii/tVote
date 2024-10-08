import React, {useEffect, useState} from 'react';
import {AuthContext} from "./context";
import './styles/App.css'
import AppRouter from "./components/AppRouter";
import './styles/AdaptiveStyles.css'
import {Toaster} from "react-hot-toast";


const App = () => {
    const [isAuth, setIsAuth] = useState(false);
    useEffect(() => {
        if (localStorage.getItem("access_token")) {
            setIsAuth(true)
        }
    }, []);
    return (
        <div className='App'>
            <Toaster
                position="bottom-center"
                reverseOrder={true}
                containerStyle={{fontFamily: 'Montserrat', fontWeight: 500}}
            />
            <AuthContext.Provider value={{ isAuth, setIsAuth }}>
                <AppRouter/>
            </AuthContext.Provider>
        </div>

    );
};

export default App;