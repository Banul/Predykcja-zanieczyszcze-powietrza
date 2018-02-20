package info.androidhive.appzan;

import android.location.Location;

import java.util.ArrayList;

/**
 * Created by User on 2017-11-18.
 */

public class LocationToStringConverter {


    public ArrayList<LocationModel> convertArrayToString (ArrayList<Location> arrayList){

        ArrayList<LocationModel> locationArr = new ArrayList<>();
        for (Location item : arrayList)
        {
            String longitude = String.valueOf(item.getLongitude());
            String latitude = String.valueOf(item.getLatitude());
            LocationModel locModel = new LocationModel(latitude,longitude);
            locationArr.add(locModel);
        }
        return locationArr;
    }

    public LocationModel convertToString (Location location){

        String longitude = String.valueOf(location.getLatitude());
        String latitude = String.valueOf(location.getLongitude());
        LocationModel locMod = new LocationModel(longitude, latitude);

        return locMod;
    }
}
