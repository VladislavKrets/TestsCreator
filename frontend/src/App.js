import './App.css';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Auth from "./Auth/Auth";

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route path='auth' element={<Auth />} />
        </Routes>
      </BrowserRouter>
  );
}

export default App;
