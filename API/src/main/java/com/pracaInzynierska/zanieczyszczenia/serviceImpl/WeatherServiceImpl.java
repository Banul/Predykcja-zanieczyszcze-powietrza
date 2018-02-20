package com.pracaInzynierska.zanieczyszczenia.serviceImpl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.pracaInzynierska.zanieczyszczenia.dao.WeatherDao;
import com.pracaInzynierska.zanieczyszczenia.model.DataModel;
import com.pracaInzynierska.zanieczyszczenia.service.WeatherService;

@Service
public class WeatherServiceImpl implements WeatherService {

	@Autowired
	WeatherDao weatherDao;

	public List<DataModel> getAllData() {
		return weatherDao.getAllData();
	}

	public List<DataModel> getAllCurrentAndPredictedData() {

		return weatherDao.getAllCurrentAndPredictedData();
	}

	public List<DataModel> getDataForSpecifiedStation(int id) {

		return weatherDao.getDataForSpecifiedStation(id);

	}

}
