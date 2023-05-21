import './Auth.css'
import CredentialsInput from "../CredentialsInput/CredentialsInput";

function Auth(props) {
    return <div className={'auth-container'}>
        <CredentialsInput setToken={props.setToken} authenticate={props.authenticate}/>
    </div>
}

export default Auth;