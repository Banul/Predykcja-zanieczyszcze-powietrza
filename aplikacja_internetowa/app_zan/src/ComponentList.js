
import React from 'react';
import StationListItem from './ItemList';

const ComponentList = (props) => {

    const ItemList = props.stationsId.map(stationId => {

        return <StationListItem
            onItemClicked = {props.onItemClicked}
            stationId = {stationId}
            stationName = {props.stationNames[stationId-1]}
            changeStationName = {props.changeStationName}
            key = {stationId}
        />
    });


    return(
    <div className = "mycontainer">
         {ItemList} 
    </div>
    );
};

export default ComponentList;