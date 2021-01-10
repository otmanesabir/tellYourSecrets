import React, {useState} from 'react';
import {authMethods} from '../authMethods'

export const firebaseAuth = React.createContext()

const AuthProvider = (props) => {
    const [inputs, setInputs] = useState({email: '', password: ''})
    const [errors, setErrors] = useState([])
    const [token, setToken] = useState(null)

    const handleSignup = () => {
        console.log('handleSignup')
        return authMethods.signup()
    }
    
    return (
      <firebaseAuth.Provider
      value={{
        handleSignup,
        inputs,
        setInputs,
      }}>
        {props.children}
  
      </firebaseAuth.Provider>
    );
  };

export default AuthProvider;
