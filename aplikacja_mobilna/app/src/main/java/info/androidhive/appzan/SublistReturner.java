package info.androidhive.appzan;

import java.util.ArrayList;



public class SublistReturner {

    public ArrayList<ItemToList> returnSublist (ArrayList <ItemToList> fullItemsList, String id){

        ArrayList <ItemToList> sublist = new ArrayList<>();

        for (ItemToList object : fullItemsList){
            if (object.getStationId().equals(id)){
                sublist.add(object);
            }
        }
        return sublist;
    }
}
