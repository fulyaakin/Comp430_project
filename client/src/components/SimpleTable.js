import React from 'react';
import SimpleTableComponent from "reactjs-simple-table";

export default function SimpleTable(props) {

  var rows = [];
  const genders = Object.values(props.data.gender);
  const addresses = Object.values(props.data.address);
  const restaurants = Object.values(props.data.restaurant); 
  const costs = Object.values(props.data.cost);
  let columns = [];

  if(localStorage.getItem("username")=="Analyst1"){
    columns.push({
      field: "gender",
      headerName: "Gender"
    },
    {
      field: "address",
      headerName: "Address"
    },
    {
      field: "restaurant",
      headerName: "Restaurant"
    },
    {
      field: "cost",
      headerName: "Cost"
    });
    genders.map(( listValue, index ) => {
      rows.push({gender:listValue,address:addresses[index],restaurant:restaurants[index],cost: costs[index]})
    }) 
  } else {
    columns.push({
      field: "gender",
      headerName: "Gender"
    },
    {
      field: "restaurant",
      headerName: "Restaurant"
    },
    {
      field: "cost",
      headerName: "Cost"
    });
    genders.map(( listValue, index ) => {
      rows.push({gender:listValue,restaurant:restaurants[index],cost: costs[index]})
    }) 
  }

  return (
    <div className="container">
      <h3>{props.title}</h3>
      <SimpleTableComponent columns={columns} list={rows} />
    </div>
  );
}