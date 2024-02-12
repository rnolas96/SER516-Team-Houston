import React from 'react'
import { useEffect, useState } from 'react';
import axios from 'axios';
import '../App.css'
import SidebarMenu from './SidebarMenu'

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
    <div className='container-full'>
      <SidebarMenu />
      <div className='route-container'>
        {!loginState?
          <div style={{display: "flex", flexDirection:"column", justifyContent: "space-between"}}>
            <input value={userName} onChange={onChangeUserName} style={{backgroundColor: "gray", marginBottom: "20px"}}/>
            <input value={password} onChange={onChangePassword}  style={{backgroundColor: "gray", marginBottom: "20px"}}/>
            <button style={{backgroundColor: "blue"}} onClick = {() => setAuthToken()}>Submit</button>
          </div>
        : <div>
            <span className=' teamName'>SER-516 Team Houston</span><br/>
            <span className=' heading'>Contributors:</span><br/>
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
