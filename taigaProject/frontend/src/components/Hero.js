import React from 'react'
import '../App.css'
import SidebarMenu from './SidebarMenu'

export default function Hero() {
  return (
    <div className='container-full'>
      <SidebarMenu />
      <div className='route-container'>
        <div>
          <span className=' teamName'>SER-516 Team Houston</span><br/>
          <span className=' heading'>Contributors:</span><br/>
          Raajveer Khattar<br/>
          Rahul Manoj<br/>
          Akash Vijayasarathy<br/>
          Vedang Sharma<br/>
          Siddesh Shetty<br/>
        </div>
      </div>    
    </div>
  )
}
