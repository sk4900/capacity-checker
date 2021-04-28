import React from 'react';
import styles from './App.css';

import endpoint from "./cdk-outputs.json"


export default class App extends React.Component {

  state = {
    status: null,
    //status_code: null,
    room_number: null,
    building_number: null,
    max_capacity: null,
    curr_capacity: null
  };

  async componentDidMount() {
    const url = endpoint.HelloCdkStack.Endpoint8024A810;
    console.log(url);
    // const response = await fetch(url);
    // var data = await response.json();
    
    try {
      setInterval(async () => {
        const response = await fetch(url);
        const data = await response.json();
        console.log("it ranerino");
        this.setState({
          //status_code: data.status_code,
          building_number: data.building_number, 
          room_number: data.room_number,
          max_capacity: data.max_capacity,
          curr_capacity: data.curr_capacity,
          status: data.status
        })
      }, 5000);
    } catch(e) {
      console.log(e);
    }

    // this.setState({
    //   //status_code: data.status_code,
    //   building_number: data.building_number, 
    //   room_number: data.room_number,
    //   max_capacity: data.max_capacity,
    //   curr_capacity: data.curr_capacity,
    //   status: data.status
    // });
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

 

  colorpicker () {
    let green = "#5af542";
    let yellow = "#fff23d";
    let red = "#ff2605";

    if (this.state.status == "red"){
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

        
        <div class="main-page">
          <h1 id="main-head">Capacity Checkr</h1>

          <h2 class="sub-head">Building: {this.state.building_number} </h2>
          <h2 class="sub-head">Room number:  {this.state.room_number}</h2>
          <h2 class="color-code-head">Color code: </h2>

          <div id="color-code-box" style={{backgroundColor: this.colorpicker()}} ></div>

          <h2 class="color-code-head">Current Occupancy: {this.state.curr_capacity} </h2> 
          <h2 class="color-code-head">Max Occupancy: {this.state.max_capacity}</h2> 
          

          {/* <div class="occupancy-pie-chart">
            <PieChart 
              animate={true}
              label={({ dataEntry }) => `${Math.round(dataEntry.percentage)} %`}
              data={[
                { title: 'Occupied spots', value: parseInt(this.state.curr_capacity), color: '#fa0000'}, //occupied
                { title: 'Free spots', value: parseInt(this.state.max_capacity), color: '#3efa00' }, //free
              ]}
            />
          </div> */}
        </div>
        

      </div>

    );
  }

}