import React from 'react'

const StationListItem = (props) => {

    return (
        <button  type="button"  className="btn btn-primary myButton col-sm-2 " onClick = {() => {props.onItemClicked(props.stationId);props.changeStationName(props.stationName) }}>
            {props.stationName}
        </button>
    )
};

export default StationListItem;

