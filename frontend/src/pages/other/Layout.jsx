import React from 'react';
import {Outlet, useLocation} from "react-router-dom";
import MyNavbar from "../../components/UI/navbar/myNavbar";
import '../../styles/components/Layout.css'

const Layout = () => {
    let location = useLocation();
    return (
        <div className={location.pathname === '/login' ? 'background-img' : 'background-gradient' }>
            <MyNavbar/>
            <Outlet/>
        </div>
    );
};

export default Layout;