import React from 'react'
import { useEffect, useState } from 'react';
import axios from 'axios';
import '../App.css'

export default function Hero() {

  const [loginState, setLoginState] = useState(false);
  const [userName, setUserName] = useState("")
  const [password, setPassword] = useState("")

  const onChangeUserName = (event) => {
    setUserName(event.target.value);
  };

  const onChangePassword = (event) => {
    setPassword(event.target.value);
  };

  function setAuthToken() {
    axios.post("/api/login" , {
      "type": "normal",
      "username": userName,
      "password": password 
    }).then(res => {
        console.log("res", res.data);
        if(res.data[0]) {
          localStorage.setItem('authToken', res.data[2])
          setLoginState(true);
        }
        else {
          alert("authentication failed");
        }
      }
    );
  }

  useEffect (() => {

    const authToken = localStorage.getItem('authToken');

    if (authToken) {
      setLoginState(true)
    }
    else {
      setLoginState(false)
    }

  }, [])
  
  return (
    <div className='container-full bg-white'>
      <div className='route-container'>
        {!loginState?
          <div style={{display: "flex", flexDirection:"column", justifyContent: "space-between"}}>
            <span className='text-[1.2rem] font-bold font-sans'>Username:</span>
            <input className='bg-white border-2 rounded-xl hover:rounded-lg duration-300 border-[#ffd053] active:border-[#ffd053] h-[2.3rem] px-3 text-[1rem] font-sans' type='username' value={userName} onChange={onChangeUserName} aria-label='username' style={{marginBottom: "20px"}}/>
            <span className=' text-[1.2rem] font-bold font-sans'>Password:</span>
            <input className='bg-white border-2 rounded-xl hover:rounded-lg duration-300 border-[#ffd053] active:border-[#ffd053] h-[2.3rem] px-3' type='password' value={password} onChange={onChangePassword} style={{marginBottom: "20px"}}/>
            <button className=' p-4 border-4 border-[#ffd053] hover:bg-[#ffd053] duration-300 hover:text-white font-sans font-bold rounded-2xl hover:rounded-lg' onClick = {() => setAuthToken()}>Submit</button>
          </div>
        : <div className=' text-left text-xl font-medium align-center mx-auto font-sans'>
            <p className=' text-4xl font-bold'>SER-516 Team Houston</p><br/>
            <p className=' text-3xl mt-[-0.5rem] mb-[-1rem] font-semibold'>Contributors:</p><br/>
            Raajveer Khattar<br/>
            Rahul Manoj<br/>
            Akash Vijayasarathy<br/>
            Vedang Sharma<br/>
            Siddesh Shetty<br/>
          </div> 
        }
      </div>    
    </div>
  )
}
