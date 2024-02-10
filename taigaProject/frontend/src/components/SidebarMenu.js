import React from 'react'
// import { Sidebar } from 'flowbite-react'
import { Sidebar, Menu, MenuItem, SubMenu } from 'react-pro-sidebar';
import { RxHamburgerMenu } from "react-icons/rx";
import '../App.css'
import { Link } from 'react-router-dom';

export default function SidebarMenu() {
  return (
    <div className='bg-blue-950'>
      <div className='h-[100%] bg-blue-950 border-r-4 border-blue-900'>
      <div className='pt-6 pb-3 pl-5'>
        <span className='text-white bg-red hover:opacity-50 transition-opacity'><RxHamburgerMenu /></span>
      </div>
      <Sidebar className='w-[100%] bg-blue-950'>
        <Menu className='bg-blue-950 text-white font-sans font-medium'>
          <Link to="/">
            <MenuItem className='hover:text-blue-950'>
              Home
            </MenuItem>
          </Link>
          <Link to="/burndowncharts">
            <MenuItem className='hover:text-blue-950'>
              Burndown Charts
            </MenuItem>
          </Link>
          <Link to="/cycletime">
            <MenuItem className='hover:text-blue-950'>
              Cycle Time
            </MenuItem>
          </Link>
          <Link to="/leadtime">
            <MenuItem className='hover:text-blue-950'>
              Lead Time
            </MenuItem>
          </Link>
        </Menu>
      </Sidebar>;
      </div>
        
    </div>
  )
}
