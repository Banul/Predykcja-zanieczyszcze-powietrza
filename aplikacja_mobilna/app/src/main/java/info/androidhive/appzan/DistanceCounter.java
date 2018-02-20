package info.androidhive.appzan;

import android.location.Location;

import java.util.ArrayList;

public class DistanceCounter {

   private ArrayList <Location> locations = new ArrayList<>();
   private ArrayList <Float> distances = new ArrayList<>();


    public void setArray ()
    {
        Location wokalna = new Location("wokalna");
        wokalna.setLatitude(52.161249);
        wokalna.setLongitude(21.032990);

        Location marszalkowska = new Location("marszalkowska");
        marszalkowska.setLatitude(52.224210);
        marszalkowska.setLongitude(21.014937);

        Location alejaNiep = new Location("niepodleglosci");
        alejaNiep.setLatitude(52.219298);
        alejaNiep.setLongitude(21.004724);

        Location wierzejewskiego = new Location("wierzejewskiego");
        wierzejewskiego.setLatitude(52.080625);
        wierzejewskiego.setLongitude(21.111186);

        Location brzozowa = new Location("brzozowa");
        brzozowa.setLatitude(52.115725 );
        brzozowa.setLongitude(21.237297);

        locations.add(wokalna);
        locations.add(marszalkowska);
        locations.add(alejaNiep);
        locations.add(wierzejewskiego);
        locations.add(brzozowa);
    }

    public ArrayList<Float> getDistancesArray (Location myLocation)
    {
        for (Location item : this.locations)
        {
            distances.add(myLocation.distanceTo(item));
        }

        return this.distances;
    }

    public ArrayList<Location> getLocations()
    {
        return this.locations;
    }


}
