package info.androidhive.appzan;


import java.util.ArrayList;

/**
 * Created by User on 2017-11-19.
 */

public class CurrentPollutionReturner {


    public ArrayList<Double> returnPm10(ArrayList <ItemToList> fullItemsList){
        ArrayList<Double> pm10List = new ArrayList<>();
        for (int i =1; i<6; i++) {
            String id = String.valueOf(i);
            SublistReturner returner = new SublistReturner();
            ArrayList<ItemToList> sublist= returner.returnSublist(fullItemsList, id);
            pm10List.add(Double.parseDouble(sublist.get(0).getPm10()));
        }
            return pm10List;
    }

    public ArrayList<Double> returnPm25(ArrayList <ItemToList> fullItemsList){
        ArrayList<Double> pm25List = new ArrayList<>();
        for (int i =1; i<6; i++) {
            String id = String.valueOf(i);
            SublistReturner returner = new SublistReturner();
            ArrayList<ItemToList> sublist= returner.returnSublist(fullItemsList, id);
            pm25List.add(Double.parseDouble(sublist.get(0).getPm25()));
        }
        return pm25List;
    }
}
