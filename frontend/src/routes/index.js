import Index from "../pages/IndexPage";
import LoginPage from "../pages/LoginPage"
import Layout from "../pages/other/Layout";
import NoMatch from "../pages/other/NoMatch";
import IndexPage from "../pages/IndexPage";

const publicRoutesWithoutNavbar = [
    {
        element: <IndexPage/>,
        path: "/",
    },
    {
        element: <LoginPage/>,
        path: "/login",
    }
]

const privateRoutesWithoutNavbar = [
    {
        element: <Index/>,
        path: "/",
    }
]

const getRoutes = (routesWithoutNavbar) => {
    return [
        {
            element: <Layout/>,
            path: "/",
            children: [...routesWithoutNavbar,
                {
                    element: <NoMatch/>,
                    path: "*"
                }]
        },

    ]
}

export const publicRoutes = getRoutes(publicRoutesWithoutNavbar)
export const privateRoutes = getRoutes(privateRoutesWithoutNavbar)
