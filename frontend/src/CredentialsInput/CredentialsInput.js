import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import CSRFToken from "../CSRFToken/CSRFToken";
import cookie from "react-cookies";

function CredentialsInput(props){

    const authenticate = (event) => {
        event.preventDefault()
        const loginData = {
            username: event.target[0].value,
            password: event.target[1].value
        }
        props.authenticate(loginData)
            .then(data => {
                props.setToken(data.data.token)
                cookie.save("token", data.data.token, {maxAge: 60*60*24*365})
            }).catch(e => {
            props.setToken(null)

        })
    }

    return <Form className={'credentials-container'} method={'POST'} onSubmit={authenticate}>
        <Form.Group className="mb-3">
            <Form.Label>Имя пользователя</Form.Label>
            <Form.Control placeholder="Имя пользователя" name={"username"} autocomplete="off"/>
        </Form.Group>
        <Form.Group className="mb-3">
            <Form.Label>Пароль</Form.Label>
            <Form.Control type="password" placeholder="Пароль" name={"password"} autocomplete="off"/>
        </Form.Group>
        <Button variant="primary" type="submit">
            {props.authButton}
        </Button>
    </Form>
}

export default CredentialsInput;