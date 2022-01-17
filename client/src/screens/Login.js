import React from 'react';
import { useState, useEffect} from 'react';
import { Col, Row, Form,FormControl, Button } from '@themesberg/react-bootstrap';
import Background from '../assets/login-bg.jpg';
import { Navigate } from 'react-router-dom';

const styles = {
    header: {
      backgroundImage: "url(" + Background + ")",
      height: '100vh',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      backgroundSize: 'cover',
      overflow:"hidden"
    },
  
    content: {
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      color: 'white',
      textAlign:"center", 
      marginLeft:"20vw", 
      marginRight:"20vw",
    },
    inputbox : {
        borderRadius:"10px",
        marginBottom:"4vh",
        textAlign:"center",
        fontSize:"2vw"
    }
  }


export default function LoginScreen() {

  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [path, setPath] = useState("/");
  const [isAlert, setAlert] = useState(false);

  useEffect(() => {
    localStorage.setItem("username", username);
  }, [username]);

  const login = () => {
    setPath("/home");
  };

    return (
    <div style={styles.header}>
        <h1 style={{"textAlign":"center","marginBottom":"0.5vw","color":"white","fontSize":"8vh"}}><br/>Online Market Analysis Tool</h1>
        <div style={styles.content}><br/>
        <Form>
            <Form.Group style={styles.inputbox} className="mb-3" controlId="exampleForm.ControlInput1">
                <Form.Label>User Name</Form.Label><br/>
                <FormControl 
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="username"
                    style={{"borderRadius":"10px","width":"15vw","height":"2.5vw","textAlign":"center","fontSize":"1.2vw"}}
                />
            </Form.Group>
            <Form.Group style={styles.inputbox} as={Row} className="mb-3" controlId="formPlaintextPassword">
                <Form.Label column sm="2">
                    Password
                </Form.Label><br/>
                <Col sm="10">
                <FormControl 
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="password"
                    style={{"borderRadius":"10px","width":"15vw","height":"2.5vw","textAlign":"center","fontSize":"1.2vw"}}
                />
                </Col>
            </Form.Group>
        </Form>
        <Button style={{"width":"10vw","height":"5vh","borderRadius":"10px","fontSize":"1.8vw","marginBottom":"5vw"}} onClick={login}>
            <strong>LOGIN</strong>
            {path == "/home" ? <Navigate to="/home" /> : null}
        </Button>

        </div>
    </div>
    );
}