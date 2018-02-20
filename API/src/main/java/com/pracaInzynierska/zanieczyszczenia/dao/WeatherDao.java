package com.pracaInzynierska.zanieczyszczenia.dao;

import java.util.List;

import com.pracaInzynierska.zanieczyszczenia.model.DataModel;

public interface WeatherDao {

	public List<DataModel> getAllData();
	public List<DataModel> getAllCurrentAndPredictedData();
	public List<DataModel> getDataForSpecifiedStation(int id);
	
}
