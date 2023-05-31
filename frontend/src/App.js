import './App.css';
import {BrowserRouter, Navigate, Route, Routes, useLocation} from "react-router-dom";
import Auth from "./Auth/Auth";
import 'bootstrap/dist/css/bootstrap.min.css';
import {useState} from "react";
import axios from './api'
import cookie from "react-cookies";
import PrivateRoute from "./PrivateRoute/PrivateRoute";
import Main from "./Main/Main";

function App() {
  let cookieToken = cookie.load("token")
  const [token, setToken] = useState(cookieToken || null);

    const authenticate = (loginData) => {
        return axios.post('login/', loginData, {
            headers: {
                "X-CSRFTOKEN": cookie.load("csrftoken")
            }
        });
    }

    const completeRegistration = (registrationData) => {
        return axios.put('login/', registrationData, {
            headers: {
                "X-CSRFTOKEN": cookie.load("csrftoken")
            }
        });
    }

  return (
      <BrowserRouter>
        <Routes>
          <Route path='auth' element={<Auth setToken={setToken} authenticate={authenticate} authButton={'Авторизация'}/>} />
          <Route path='registration' element={<Auth setToken={setToken} authenticate={completeRegistration} authButton={'Регистрация'}/>} />
          <Route path='main' element={
              <RequireAuth token={token}>
                  <Main/>
              </RequireAuth>
          }/>
        </Routes>
      </BrowserRouter>
  );
}

function RequireAuth(props) {
  let location = useLocation();

  if (!props.token) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to when they were redirected. This allows us to send them
    // along to that page after they login, which is a nicer user experience
    // than dropping them off on the home page.
    return <Navigate to="/auth" state={{ from: location }} replace />;
  }

  return props.children;
}

export default App;
