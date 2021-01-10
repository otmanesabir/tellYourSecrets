import React, {useContext} from 'react';
import {firebaseAuth} from './firebase/provider/AuthProvider'
import logo from './logo.svg';
import './App.css';
import {Route, Switch} from 'react-router-dom'
import Signup from './components/Signup'

function App() {
  const {handleSignup} = useContext(firebaseAuth)
  console.log(handleSignup)
  return (
    <>
    {/* switch allows switching which components render.  */}
      <Switch>
        {/* route allows you to render by url path */}
        <Route exact path='/' component={Signup} />

      </Switch>
    </>
  );
}

export default App;
