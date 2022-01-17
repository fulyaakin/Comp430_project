import React, {useEffect,useState} from 'react';
import {Col, Card,Button} from '@themesberg/react-bootstrap';

function StatsCard(props) {

  const idToken = localStorage.getItem("idToken");
  const [cardData, setCardData] = useState([]);

  return (
    <Card style={{ width: '25rem', height: '10rem',backgroundColor:'gray',marginTop:'0.1vw', margin:'1vw', border: "10px", borderRadius:"15px"}}>
  <Card.Img />
  <Card.Body style={{"fontSize":"20px","color":"white","textAlign":"center"}}>
    <Card.Title>{props.title}</Card.Title>
    <Card.Text style={{"fontSize":"30px"}}><br/>
    <strong>{props.number}</strong>
    </Card.Text>
  </Card.Body>
</Card>
  );
}

export default StatsCard;
