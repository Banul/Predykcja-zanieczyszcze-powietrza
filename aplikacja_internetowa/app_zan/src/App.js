import React, { Component } from 'react';
import axios from 'axios';
import './App.css';
import { LineChart, XAxis, YAxis, CartesianGrid, Line, Tooltip, ResponsiveContainer,Label,ReferenceLine } from 'recharts';
import ComponentList from './ComponentList';



export default class App extends Component {

  constructor(){
    super();
    this.state = {
      selectedStation : 1,
      selectedStationName:'Wokalna',
      arrPM25 : [],
      arrPM : []
    }
      this.fetchData(1);
  }



 fetchData(number){
  axios.get(`http://inzyniercorazblizej.eu-central-1.elasticbeanstalk.com/pastAndFutureData/${number}`).then(results => {
        const datesToPlot = results.data.map(obj => obj.date.substring(8,10)+"."+obj.date.substring(5,7) +" " + obj.date.substring(10,16));
        const pm25ToPlot = results.data.map(obj => obj.pm25);
        const pm10ToPlot = results.data.map(obj => obj.pm10);
        
  const arrResult = [];

  for (let iterator = 0; iterator < datesToPlot.length; iterator++){
    arrResult.push({
      date : datesToPlot[iterator],
      pm25 : pm25ToPlot[iterator],
      pm10 : pm10ToPlot[iterator]


    });
  };
 
     this.setState({
          arrPM25 : arrResult.map(obj => ({ date : (obj.date), pm25 : (obj.pm25)}    )),
          arrPM : arrResult.map(obj => ({ date : (obj.date), pm10 : (obj.pm10)}    ))
        });

        
  }
  )
}


  render() {

    return (
      <div className="App">
         <h1> Wybrana stacja: {this.state.selectedStationName} </h1>

          <ComponentList
      onItemClicked = {(idNumber) => {this.fetchData(idNumber)} }
      stationsId = {[1,2,3,4,5]}
      stationNames = {["Wokalna", "Marszałkowska", "Al.Niepodległości", "Wierzejewskiego", "Brzozowa"]}
      changeStationName = {(stationName) => {this.setState({selectedStationName : stationName})}}
      />

<div className="myText">
        <h2>Wykres stężenia pyłu zawieszonego PM25 [mikrogramy/metr sześcienny] w czasie:</h2>
</div>
      <div className = "chartsContainer">
        <ResponsiveContainer width ="100%" height = {400} margin={{ right:30 }}> 
         <LineChart height={400} data={this.state.arrPM25}>
    <XAxis dataKey="date" angle={-60} textAnchor="end" interval = {4} height={200}/>
    <YAxis>
     <Label value="[ug/m^3]" angle={270}/>
    </YAxis>
    <CartesianGrid stroke="#eee" strokeDasharray="5 5"/>
    <Tooltip/>
    <ReferenceLine y={25} label="Dopuszczalne stężenie" stroke="red"/>
    <Line type="monotone" dataKey="pm25" stroke="#8884d8" />
  </LineChart>
  </ResponsiveContainer>

      <h2>Wykres stężenia pyłu zawieszonego PM10 [mikrogramy/metr sześcienny] w czasie:</h2>
   <ResponsiveContainer width ="100%" height = {400} margin={{ right:30 }}> 
         <LineChart height={400} data={this.state.arrPM}>
    <XAxis dataKey="date"  angle={-60} textAnchor="end" interval = {4} height={200}/>
    <YAxis>
     <Label value="[ug/m^3]" angle={270}/>
    </YAxis>
    <CartesianGrid stroke="#eee" strokeDasharray="5 5"/>
    <Tooltip/>
    <ReferenceLine y={50} label="Dopuszczalne stężenie" stroke="red"/>
    <Line type="monotone" dataKey="pm10" stroke="#8884d8" />
  </LineChart>
  </ResponsiveContainer>

      </div>
      </div>
    );
  }
}