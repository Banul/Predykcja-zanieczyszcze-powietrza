package info.androidhive.appzan;

/**
 * Created by User on 2017-11-18.
 */

public class LocationModel {

    private String latitude;
    private String longitude;

    LocationModel (String lat, String lon){
        this.latitude = lat;
        this.longitude = lon;
    }

    @Override
    public String toString(){
        return String.valueOf(latitude) + " " + String.valueOf(longitude);
    }
}
