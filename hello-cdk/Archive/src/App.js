import React from 'react';
import './css/style.css';
export default class App extends React.Component {
  state = {
    status: null,
    //status_code: null,
    room_number: null,
    building_number: null,
    max_capacity: null,
    curr_capacity: null
  };
  // async componentDidMount() {
  //   const url = "https://j7inraenr5.execute-api.us-east-1.amazonaws.com/prod/";
  //   const response = await fetch(url);
  //   var data = await response.json();
  //   try {
  //     setInterval(async () => {
  //       const response = await fetch(url);
  //       const data = await response.json();
  //       console.log("it ranerino");
  //       this.setState({
  //         //status_code: data.status_code,
  //         building_number: data.building_number,
  //         room_number: data.room_number,
  //         max_capacity: data.max_capacity,
  //         curr_capacity: data.curr_capacity,
  //         status: data.status
  //       })
  //     }, 1000);
  //   } catch(e) {
  //     console.log(e);
  //   }
  //   this.setState({
  //     //status_code: data.status_code,
  //     building_number: data.building_number,
  //     room_number: data.room_number,
  //     max_capacity: data.max_capacity,
  //     curr_capacity: data.curr_capacity,
  //     status: data.status
  //   });
  // }
  colorpicker () {
    let green = "#5AF542";
    let yellow = "#FFF23D";
    let red = "#FF2605";
    if (this.state.status === "red"){
      return red;
    }
    else if (this.state.status === "yellow") {
      return yellow;
    }
    else {
      return green;
    }
  }
  render() {
    return (
      <div>
        <div className="main-page">
          <h1 id="main-head">Capacity Checkr</h1>
          <h2 className="sub-head">Building: {this.state.building_number} </h2>
          <h2 className="sub-head">Room number:  {this.state.room_number}</h2>
          <h2 className="color-code-head">Color code: </h2>
          <div id="color-code-box" style={{backgroundColor: this.colorpicker()}} ></div>
          <h2 className="color-code-head">Current Occupancy: {this.state.curr_capacity} </h2>
          <h2 className="color-code-head">Max Occupancy: {this.state.max_capacity}</h2>
        </div>
      </div>
    );
  }
}