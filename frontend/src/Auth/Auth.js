import './Auth.css'
import CredentialsInput from "../CredentialsInput/CredentialsInput";

function Auth(props) {
    return <div className={'auth-container'}>
        <CredentialsInput setToken={props.setToken} authenticate={props.authenticate} authButton={props.authButton}/>
    </div>
}

export default Auth;