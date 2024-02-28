import React from 'react'
import { Sidebar, Menu, MenuItem, useProSidebar, menuClasses, sidebarClasses } from "react-pro-sidebar";

import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import ShowChartIcon from '@mui/icons-material/ShowChart';
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";
import HubIcon from '@mui/icons-material/Hub';
import '../App.css'
import { Link } from 'react-router-dom';
import SvgIcon from './reusable_components/SvgIcon';


export default function SidebarMenu() {
  
  const { collapseSidebar, toggleSidebar, collapsed, toggled, broken } = useProSidebar();
  
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
    <div className='font-sans font-semibold'>
    <div id="app" style={({ height: "100vh" }, { display: "flex", flexDirection: "row" })}>
    <Sidebar
        rootStyles={{
          borderColor: "white",
          // backgroundColor: 'rgb(0, 249, 249)'
          ['.' + menuClasses.button]: {
            '&:hover' : {
              backgroundColor: '#ffe59f',
              transitionDuration: '0.3s',
            }
          }
        }}
        backgroundColor="white"
        style={{ height: "100vh"}}>
      <Menu
        menuItemStyles={{
          button: {
            ['&.active']: {
              backgroundColor: '#ffe59f',
              color: '#ffe59f'
            }
          }
        }}
      >
        <MenuItem
          className='mI'
          icon={<MenuOutlinedIcon />}
          
          onClick={() => {
            collapseSidebar();
          }}
          style={{ textAlign: "center" }}
         >
          {" "}
         </MenuItem>

        <MenuItem className='mI' icon={<HomeOutlinedIcon />} component={<Link to={"/"} />}>Home</MenuItem>
        <MenuItem className='mI' icon={<ShowChartIcon />} component={<Link to={"/burndowncharts"} />}>Burndown Charts</MenuItem>
        <MenuItem className='mI' icon={<SvgIcon name="boxplot" className="w-4 white" />} component={<Link to={"/cycletime"} />}>Cycle Time</MenuItem>
        <MenuItem className='mI' icon={<SvgIcon name="boxplot" className="w-4 white" />} component={<Link to={"/leadtime"} />}>Lead Time</MenuItem>
      </Menu>
    </Sidebar>
    </div>
    </div>
  )
}
