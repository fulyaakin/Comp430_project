import React, { useState, useReducer, useEffect} from "react";
import { Link, Navigate } from "react-router-dom";

function NavigationBar() {

  const styles = {
    content: {
      backgroundColor: '#02A684',      
      display: "flex",
      justifyContent: "space-between",
      color: "white",
      fontSize:"1.8vw",
      margin:"0",
      fontFamily:"sans-serif"
    },
  }

  return (
    <div className="container" style={styles.content}>
         <h4 style={{"paddingLeft":"2vw","color":'white'}}>Welcome {localStorage.getItem("username")}</h4>
        <nav>
            <ul style={{"display":"flex","justifyContent":"space-between"}}>
                <span><Link to="/" style={{ textDecoration: 'none', color:'white', paddingRight:"2vw" }}><strong>Logout</strong></Link></span>
            </ul>
        </nav>
    </div>
    );
}

export default NavigationBar;
