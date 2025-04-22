import React, { useState,useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { auth } from '../helpers/firebase';
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword
} from 'firebase/auth';
import '../../style/Login.css';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignup, setIsSignup] = useState(false);
  const [error, setError] = useState('');
  const [isLoading,setIsLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(()=>{
    const unsubscribe = auth.onAuthStateChanged((user)=>{
      if(user){
        navigate('/home')
      }
    })
  })

  const handleAuth = async () => {
    setError('');
    setIsLoading(true);
  
    if (!email || !password) {
      setError("Please enter both email and password");
      return;
    }
  
    try {
      let userCredential;
      if (isSignup) {
        userCredential = await createUserWithEmailAndPassword(auth, email, password);
      } else {
        userCredential = await signInWithEmailAndPassword(auth, email, password);
      }  
      alert("Login successfull");
      navigate('/home');
    } catch (err) {
      setError(err.message);
    }
    finally{
      setIsLoading(false);
    }
  };
  
  return (
    <div className="login-container">
      <div className="login-card">
        <h2>{isSignup ? 'Create Account' : 'Welcome Back'}</h2>
        <p className="login-subtitle">
          {isSignup ? 'Sign up to access the dashboard' : "Sign in to continue to Parkinson's Dashboard"}
        </p>

        <div className="form-group">
          <label>Email Address</label>
          <input
            type="email"
            placeholder="batman@gothamsaver.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        {error && <p className="error">{error}</p>}

        <button className="login-button" onClick={handleAuth} disabled={isLoading} >
          {isSignup ? 'Sign Up' : 'Log In'}
        </button>

        <p style={{ marginTop: "1rem" }}>
          {isSignup ? "Already have an account?" : "Don't have an account?"}
          <span
            onClick={() => setIsSignup(!isSignup)}
            style={{ color: "#007bff", cursor: "pointer", marginLeft: "5px" }}
          >
            {isSignup ? 'Login' : 'Sign up'}
          </span>
        </p>

        <p className="footer">
          © {new Date().getFullYear()} Parkinson's Predictor. All rights reserved.
        </p>
      </div>
    </div>
  );
}
