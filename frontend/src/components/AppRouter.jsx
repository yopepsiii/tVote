import React, {useContext} from 'react';
import {createBrowserRouter, RouterProvider, useLocation} from "react-router-dom";
import {privateRoutes, publicRoutes} from "../routes";
import {AuthContext} from "../context";


const AppRouter = () => {
    const {isAuth} = useContext(AuthContext);
    const router = createBrowserRouter(isAuth ? privateRoutes : publicRoutes )
    return (
        <div>
            <RouterProvider router={router}/>
        </div>

    );
};

export default AppRouter;