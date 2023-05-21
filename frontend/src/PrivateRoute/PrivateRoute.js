import {Route, Navigate} from "react-router-dom";

function PrivateRoute(props) {
    return <Route {...props}>
        {
            !props.token ? <Navigate to="/auth/"/> :
                <>
                    {props.children}
                </>
        }
    </Route>
}