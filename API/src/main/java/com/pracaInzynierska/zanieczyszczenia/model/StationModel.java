package com.pracaInzynierska.zanieczyszczenia.model;
import java.util.List;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import javax.persistence.Table;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

/**
 * Zaimplementowane przy pomocy:
 *  https://stackoverflow.com/questions/41582979/how-to-ignore-handler-hibernatelazyinitializer-in-json-jackson-in-s
 * 
 * @author User
 *
 */

@Entity
@Table(name = "station_info")
@JsonSerialize
//@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "id")
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})


public class StationModel {
	
	@Id
	@Column(name = "id")
	private int id;
	
	@Column(name = "nazwa_miejscowosci")
	private String nazwaMiejscowosci;
	
	@Column(name = "nazwa_ulicy")
	private String nazwaUlicy;
	
	@Column(name = "szerokosc_stopnie")
	private double szerokoscStopnie;
	
	@Column(name = "szerokosc_minuty")
	private double szerokoscMinuty;
	
	@Column(name = "szerokosc_sekundy")
	private double szerokoscSekundy;
	
	@Column(name = "dlugosc_stopnie")
	private double dlugoscStopnie;
	
	@Column(name = "dlugosc_minuty")
	private double dlugoscMinuty;
	
	@Column(name = "dlugosc_sekundy")
	private double dlugoscSekundy;
	
	@Column(name = "liczba_glosow")
	private int liczbaGlosow;
	
	@Column(name = "biezaca_ocena")
	private double biezacaOcena;
	
	@OneToMany(mappedBy = "stationModel")
	@JsonBackReference
	private List<DataModel> dataModel;

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getNazwaMiejscowosci() {
		return nazwaMiejscowosci;
	}

	public void setNazwaMiejscowosci(String nazwaMiejscowosci) {
		this.nazwaMiejscowosci = nazwaMiejscowosci;
	}

	public String getNazwaUlicy() {
		return nazwaUlicy;
	}

	public void setNazwaUlicy(String nazwaUlicy) {
		this.nazwaUlicy = nazwaUlicy;
	}

	public double getSzerokoscStopnie() {
		return szerokoscStopnie;
	}

	public void setSzerokoscStopnie(double szerokoscStopnie) {
		this.szerokoscStopnie = szerokoscStopnie;
	}

	public double getSzerokoscMinuty() {
		return szerokoscMinuty;
	}

	public void setSzerokoscMinuty(double szerokoscMinuty) {
		this.szerokoscMinuty = szerokoscMinuty;
	}

	public double getSzerokoscSekundy() {
		return szerokoscSekundy;
	}

	public void setSzerokoscSekundy(double szerokoscSekundy) {
		this.szerokoscSekundy = szerokoscSekundy;
	}

	public double getDlugoscStopnie() {
		return dlugoscStopnie;
	}

	public void setDlugoscStopnie(double dlugoscStopnie) {
		this.dlugoscStopnie = dlugoscStopnie;
	}

	public double getDlugoscMinuty() {
		return dlugoscMinuty;
	}

	public void setDlugoscMinuty(double dlugoscMinuty) {
		this.dlugoscMinuty = dlugoscMinuty;
	}

	public double getDlugoscSekundy() {
		return dlugoscSekundy;
	}

	public void setDlugoscSekundy(double dlugoscSekundy) {
		this.dlugoscSekundy = dlugoscSekundy;
	}

	public int getLiczbaGlosow() {
		return liczbaGlosow;
	}

	public void setLiczbaGlosow(int liczbaGlosow) {
		this.liczbaGlosow = liczbaGlosow;
	}

	public double getBiezacaOcena() {
		return biezacaOcena;
	}

	public void setBiezacaOcena(double biezacaOcena) {
		this.biezacaOcena = biezacaOcena;
	}

	public List<DataModel> getDataModel() {
		return dataModel;
	}

	public void setDataModel(List<DataModel> dataModel) {
		this.dataModel = dataModel;
	}

	
}
