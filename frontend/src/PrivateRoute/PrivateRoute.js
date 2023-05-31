import {Route, Navigate, useLocation} from "react-router-dom";

function PrivateRoute(props) {
    let location = useLocation();
    return <Route path={props.path} element={!props.token ? <Navigate to="/auth/" state={{ from: location }} replace/> : props.element}/>
}
export default PrivateRoute