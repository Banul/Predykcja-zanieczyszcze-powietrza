package com.pracaInzynierska.zanieczyszczenia.daoImpl;

import java.util.ArrayList;
import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.TypedQuery;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;

import org.springframework.stereotype.Repository;

import com.pracaInzynierska.zanieczyszczenia.dao.WeatherDao;
import com.pracaInzynierska.zanieczyszczenia.model.DataModel;

/*
 * 
 * Implementacja klasy przy wykorzystaniu strony:
 * http://www.objectdb.com/java/jpa/query/criteria
 * 
 */
@Repository
public class WeatherDaoImpl implements WeatherDao {

	@PersistenceContext
	EntityManager em;

	public List<DataModel> getAllData() {

		CriteriaBuilder cb = em.getCriteriaBuilder();
		CriteriaQuery<DataModel> cq = cb.createQuery(DataModel.class);
		Root<DataModel> root = cq.from(DataModel.class);
		TypedQuery<DataModel> q = em.createQuery(cq);
		List<DataModel> allData = q.getResultList();

		return allData;

	}
	
	public List<DataModel> getAllCurrentAndPredictedData()
	{
		CriteriaBuilder cb = em.getCriteriaBuilder();
		CriteriaQuery<DataModel> cq = cb.createQuery(DataModel.class);
		Root<DataModel> root = cq.from(DataModel.class);
		
		List<DataModel> allCurrentAndPredictedData = new ArrayList<DataModel>();
		
		for (int x = 1; x<6; x++)
		{
			cq.select(root).where(cb.equal(root.get("stationModel").get("id"), x));
			TypedQuery<DataModel> q = em.createQuery(cq);
			List<DataModel> dataAndPrediction = q.getResultList();
			dataAndPrediction = dataAndPrediction.subList(dataAndPrediction.size()-6, dataAndPrediction.size());
			for (DataModel item : dataAndPrediction)
			{
				allCurrentAndPredictedData.add(item);
			}
		}

			return allCurrentAndPredictedData;
			
	}
	
	public List<DataModel> getDataForSpecifiedStation(int id){
		
		CriteriaBuilder cb = em.getCriteriaBuilder();
		CriteriaQuery<DataModel> cq = cb.createQuery(DataModel.class);
		Root<DataModel> root = cq.from(DataModel.class);
		
		List<DataModel> allDataBySpecifiedStation = new ArrayList<DataModel>();
		

		cq.select(root).where(cb.equal(root.get("stationModel").get("id"), id));
		TypedQuery<DataModel> q = em.createQuery(cq);
		List<DataModel> dataAndPrediction = q.getResultList();
		dataAndPrediction = dataAndPrediction.subList(0, dataAndPrediction.size());
		for (DataModel item : dataAndPrediction)
		 {
			allDataBySpecifiedStation.add(item);
		 }
		
		System.out.println(allDataBySpecifiedStation.get(0).getDate());
		return allDataBySpecifiedStation;
		
	}



}
