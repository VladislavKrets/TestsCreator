import './App.css';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Auth from "./Auth/Auth";
import 'bootstrap/dist/css/bootstrap.min.css';
import {useState} from "react";
import axios from './api'
import cookie from "react-cookies";

function App() {
  const [token, setToken] = useState(null);

    const authenticate = (loginData) => {
        loginData.preventDefault();
        return axios.post('login/', loginData, {
            headers: {
                "X-CSRFTOKEN": cookie.load("csrftoken")
            }
        });
    }

  return (
      <BrowserRouter>
        <Routes>
          <Route path='auth' element={<Auth setToken={setToken} authenticate={authenticate}/>} />
        </Routes>
      </BrowserRouter>
  );
}

export default App;
