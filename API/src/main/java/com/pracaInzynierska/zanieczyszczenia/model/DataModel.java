package com.pracaInzynierska.zanieczyszczenia.model;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

/*
 * Zaimplementowane przy pomocy:
 * https://stackoverflow.com/questions/41582979/how-to-ignore-handler-hibernatelazyinitializer-in-json-jackson-in-s
 */

@Entity
@JsonSerialize
@Table(name = "final_table")
//@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "index")
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})


public class DataModel {

	@Id
	@Column(name = "index")
	@JsonProperty("index")
	private int index;
	
	@Column(name = "date")
	private String date;

	@Column(name = "cisnienie")
	private String pressure;

	@Column(name = "kierunek_wiatru")
	private String windDirection;

	@Column(name = "predkosc_wiatru")
	private String windStrength;

	@Column(name = "temperatura")
	private String temperature;

	@Column(name = "warunki_pogodowe")
	private String weatherCond;

	@Column(name = "wilgotnosc")
	private String humidity;

	@Column(name = "pm10")
	private Double pm10;

	@Column(name = "pm25" )
	private Double pm25;
	
	@ManyToOne(targetEntity = StationModel.class, fetch = FetchType.LAZY)
	@JoinColumn(name="id_stacji")
	@JsonManagedReference
	private StationModel stationModel;

	public String getDate() {
		return date;
	}

	public void setDate(String date) {
		this.date = date;
	}

	public int getIndex() {
		return index;
	}

	public void setIndex(int index) {
		this.index = index;
	}

	public StationModel getStationModel() {
		return stationModel;
	}

	public void setStationModel(StationModel stationModel) {
		this.stationModel = stationModel;
	}

	public String getPressure() {
		return pressure;
	}

	public void setPressure(String pressure) {
		this.pressure = pressure;
	}

	public String getWindDirection() {
		return windDirection;
	}

	public void setWindDirection(String windDirection) {
		this.windDirection = windDirection;
	}

	public String getWindStrength() {
		return windStrength;
	}

	public void setWindStrength(String windStrength) {
		this.windStrength = windStrength;
	}

	public String getTemperature() {
		return temperature;
	}

	public void setTemperature(String temperature) {
		this.temperature = temperature;
	}

	public String getWeatherCond() {
		return weatherCond;
	}

	public void setWeatherCond(String weatherCond) {
		this.weatherCond = weatherCond;
	}

	public String getHumidity() {
		return humidity;
	}

	public void setHumidity(String humidity) {
		this.humidity = humidity;
	}


	public Double getPm10() {
		return pm10;
	}

	public void setPm10(Double pm10) {
		this.pm10 = pm10;
	}

	public Double getPm25() {
		return pm25;
	}

	public void setPm25(Double pm25) {
		this.pm25 = pm25;
	}



	
}
