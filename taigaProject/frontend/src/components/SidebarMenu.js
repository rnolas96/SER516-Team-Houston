import React from 'react'
// import { Sidebar } from 'flowbite-react'
// import { Sidebar, Menu, MenuItem, SubMenu } from 'react-pro-sidebar';
import { Sidebar, Menu, MenuItem, useProSidebar, menuClasses } from "react-pro-sidebar";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import PeopleOutlinedIcon from "@mui/icons-material/PeopleOutlined";
import ContactsOutlinedIcon from "@mui/icons-material/ContactsOutlined";
import ReceiptOutlinedIcon from "@mui/icons-material/ReceiptOutlined";
import CalendarTodayOutlinedIcon from "@mui/icons-material/CalendarTodayOutlined";
import HelpOutlineOutlinedIcon from "@mui/icons-material/HelpOutlineOutlined";
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";
// import { RxHamburgerMenu } from "react-icons/rx";
import '../App.css'
import { Link } from 'react-router-dom';
import { colors } from '@mui/material';


export default function SidebarMenu() {
  
  const { collapseSidebar, toggleSidebar, collapsed, toggled, broken, rtl } = useProSidebar();
  
  const toggle = () => {
  toggleSidebar();
    if (toggled) {
      console.log(true);
      collapseSidebar();
    } else {
      console.log(false);
      collapseSidebar();
    }
  };
  
  return (
    // <div className="height-full">
    //   <div className='top-0 bg-blue-950'>
    //   <div className='pt-6 pb-3 pl-5'>
    //     <span className='text-white bg-red hover:opacity-50 transition-opacity'><RxHamburgerMenu /></span>
    //   </div>
    //   <Sidebar className='w-[100%]'>
    //     <Menu className='bg-blue-950 text-white font-sans font-medium'>
    //       <MenuItem className='hover:text-blue-950'>
    //         <Link to="/">
    //           Home
    //         </Link>
    //       </MenuItem>
    //       <MenuItem className='hover:text-blue-950'>
    //         <Link to="/burndowncharts">
    //           Burndown Charts
    //         </Link>
    //       </MenuItem>
    //       <MenuItem className='hover:text-blue-950'>
    //         <Link to="/cycletime">
    //           Cycle Time
    //         </Link>
    //       </MenuItem>
    //       <MenuItem className='hover:text-blue-950'>
    //         <Link to="/leadtime">
    //           Lead Time
    //         </Link>
    //       </MenuItem>
    //     </Menu>
    //   </Sidebar>
    //   </div>
        
    // </div>
    <div className='font-sans font-semibold'>
    <div id="app" style={({ height: "100vh" }, { display: "flex", flexDirection: "row" })}>
    <Sidebar
        rootStyles={{
          borderColor: "rgb(0, 249, 249)",
          // backgroundColor: 'rgb(0, 249, 249)'
          ['.' + menuClasses.button]: {
            '&:hover' : {
              backgroundColor: '#9CAF88',
              transitionDuration: '0.3s',
              // colors: '#000000',
            }
          }
        }}
        backgroundColor="rgb(0, 249, 249)"
        rtl={false}
        style={{ height: "100vh" }}>
      <Menu>
        <MenuItem
          icon={<MenuOutlinedIcon />}
          
          onClick={() => {
            collapseSidebar();
          }}
          style={{ textAlign: "center" }}
        >
          {" "}
        </MenuItem>

        <MenuItem active icon={<HomeOutlinedIcon />} component={<Link to={"/"} />}>Home</MenuItem>
        <MenuItem active icon={<PeopleOutlinedIcon />} component={<Link to={"/burndowncharts"} />}>Burndown Charts</MenuItem>
        <MenuItem active icon={<ContactsOutlinedIcon />} component={<Link to={"/cycletime"} />}>Cycle Time</MenuItem>
        <MenuItem active icon={<ReceiptOutlinedIcon />} component={<Link to={"/leadtime"} />}>Lead Time</MenuItem>
      </Menu>
    </Sidebar>
    </div>
    </div>
  )
}
