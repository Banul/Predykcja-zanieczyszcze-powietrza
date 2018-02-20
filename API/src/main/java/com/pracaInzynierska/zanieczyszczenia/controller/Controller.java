package com.pracaInzynierska.zanieczyszczenia.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.pracaInzynierska.zanieczyszczenia.model.DataModel;
import com.pracaInzynierska.zanieczyszczenia.service.WeatherService;

@RestController
public class Controller {

	@Autowired
	WeatherService weatherService;

	@RequestMapping("/alldata")
	public List<DataModel> getAllData() 
	{
		return weatherService.getAllCurrentAndPredictedData();
	}
	
	@RequestMapping("/currentDataAndPrediction")
	public List<DataModel> getAllCurrentAndPredictedData()
	{
		return weatherService.getAllCurrentAndPredictedData();
	}
	
	@CrossOrigin
	@RequestMapping("/specifiedData/{id}")
	public List<DataModel> getDataForSpecifiedStation(@PathVariable int id)
	{
		return weatherService.getDataForSpecifiedStation(id);
	}


}
