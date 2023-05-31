import React from 'react';
import cookie from "react-cookies";

const CSRFToken = () => {
    let csrftoken = cookie.load("csrftoken")
    return (
        <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
    );
};
export default CSRFToken;