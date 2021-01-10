import firebaseconfig from './firebaseIndex'
import firebase from 'firebase'

export const authMethods = {
    // firebase helper methods go here... 
    signup: (email, password) => {
        firebase.auth().createUserWithEmailAndPassword(email,password)
      .then(res => {
        console.log(res)
      })
      .catch(err => {
        console.error(err)
      })
      },
    signin: (email, password) => {
        // TODO Add Logic
      },
    signout: (email, password) => {
        // TODO Add logic
      },
    }