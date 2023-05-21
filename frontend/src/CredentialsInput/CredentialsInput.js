import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function CredentialsInput(props){

    const authenticate = (event) => {
        console.log(event)
        props.authenticate
            .then(data => {
                props.setToken(data.data.token)
            }).catch(e => {
            props.setToken(null)
        })
    }

    return <Form className={'credentials-container'} method={'POST'} onSubmit={authenticate}>
        <Form.Group className="mb-3">
            <Form.Label>Имя пользователя</Form.Label>
            <Form.Control placeholder="Имя пользователя" name={"username"}/>
        </Form.Group>
        <Form.Group className="mb-3">
            <Form.Label>Пароль</Form.Label>
            <Form.Control type="password" placeholder="Пароль" name={"password"}/>
        </Form.Group>
        <Button variant="primary" type="submit">
            Войти
        </Button>
    </Form>
}

export default CredentialsInput;