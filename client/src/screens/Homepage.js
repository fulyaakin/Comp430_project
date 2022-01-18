import React, { useState, useEffect } from "react";
import Histogram from "../components/Histogram";
import StatsCard from "../components/StatsCard";
import SimpleTable from "../components/SimpleTable";
import NavigationBar from "../components/NavigationBar";
import axios from "axios";

function Homepage() {

  const [histogram1, setHistogram1] = useState()
  const [histogram2, setHistogram2] = useState()
  const [value1, setValue1] = useState()
  const [value2, setValue2] = useState()
  const [table1, setTable1] = useState()
  const [table2, setTable2] = useState()

  useEffect(()=>{
    if(localStorage.getItem('username') === 'Analyst1'){
      axios.get(
        'http://localhost:8000/value_1').then(response => {
          setValue1(response.data.content);
          setHistogram1(response.data.content2);
          setTable1(response.data.content3);
      }).catch(error => {
        console.log(error)
      });
      
    }
    else {
      axios.get(
        'http://localhost:8000/value_2').then(response => {
          setValue2(response.data.content);
          setHistogram2(response.data.content2);
          setTable2(response.data.content3);
      }).catch(error => {
        console.log(error)
      });
      
    }
  }, [])

    let card_title='Address with Most Orders';
    let card_number = value2;
    let hist_title= 'Order Distribution through Neighborhoods';
    let hist_data = histogram2;
    let table_title = "Orders from Neighborhood with Most Orders";
    let table_data = table2;

    if(localStorage.getItem("username") === 'Analyst1'){
      card_title = 'Gender with Most Orders';
      card_number = value1;
      hist_data = histogram1;
      table_data = table1;
      table_title = "Orders of People Aged 21";
      hist_title='Order Distribution through Ages';
    }

    const [isTable, setIsTable] = useState(false);
    const [isHistogram, setIsHistogram] = useState(false);
    const [isCard, setIsCard] = useState(false);

    const handleTable = () => {
        setIsTable(!isTable);
    }

    const handleHistogram = () => {
        setIsHistogram(!isHistogram);
    }

    const handleCard = () => {
      setIsCard(!isCard);
  }
  
    return(
      <div><NavigationBar/>
        <div style={{"display":"flex","justifyContent":"center","paddingTop":"5vh"}}>
        <div>
                <span style={{"paddingRight":"10vw"}}>
                    <button onClick={handleTable} style={{"width":"20vw","height":"10vh","borderRadius":"10px","fontSize":"1.8vw","marginBottom":"3vw"}} type="submit"><strong>Table</strong></button>
                </span>
                <span style={{"paddingRight":"10vw"}}>
                    <button onClick={handleCard} style={{"width":"20vw","height":"10vh","borderRadius":"10px","fontSize":"1.8vw","marginBottom":"3vw"}} type="submit"><strong>Value</strong></button>
                </span>
                <button onClick={handleHistogram} style={{"width":"20vw","height":"10vh","borderRadius":"10px","fontSize":"1.8vw","marginBottom":"3vw"}} type="submit"><strong>Histogram</strong></button>
                <br/>
                {isTable? <SimpleTable data={table_data} title={table_title}/> : null}
                <span style={{"display":"flex","justifyContent":"center"}}>{isCard? <StatsCard title={card_title} number={card_number}/> : null}</span>
                {isHistogram? <Histogram data={hist_data} title={hist_title}/> : null}
            </div>
        </div>
      </div>
    );
}

export default Homepage;