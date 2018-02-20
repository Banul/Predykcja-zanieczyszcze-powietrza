package com.pracaInzynierska.zanieczyszczenia.service;

import java.util.List;

import com.pracaInzynierska.zanieczyszczenia.model.DataModel;

public interface WeatherService {

	public List<DataModel> getAllData();
	public List<DataModel> getAllCurrentAndPredictedData();
	public List<DataModel> getDataForSpecifiedStation(int id);

}
