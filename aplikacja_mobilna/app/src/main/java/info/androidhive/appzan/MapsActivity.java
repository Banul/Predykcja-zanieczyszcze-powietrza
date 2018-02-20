package info.androidhive.appzan;


import android.Manifest;
import android.content.pm.PackageManager;
import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.os.Looper;
import android.support.v4.app.ActivityCompat;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.LocationSettingsRequest;
import com.google.android.gms.location.SettingsClient;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.CircleOptions;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Do implementacji klasy wykorzystane zostały pewne funkcjonalności z m.in:
 * https://github.com/googlesamples/android-play-location/blob/master/LocationUpdates/app/src/main/java/com/google/android/gms/location/sample/locationupdates/MainActivity.java
 * https://github.com/sudeepag/MovieSelector/blob/master/app/src/main/java/edu/gatech/logitechs/movieselector/View/MuveeMaps.java
 * https://developer.android.com/training/location/retrieve-current.html
 * https://developer.android.com/training/location/receive-location-updates.html
 *
 * Ikony zaczerpnięte z :
 * https://icons8.com
 *
 *
 */

public class MapsActivity extends AppCompatActivity implements OnMapReadyCallback {


    private GoogleMap mMap;
    private Location currLocation = new Location("Location");
    private ArrayList<Location> stationsLocationsArray = new ArrayList<>();
    private LocationCallback mLocationCallback;
    LocationRequest mLocationRequest;
    private LocationSettingsRequest mLocationSettingsRequest;
    private SettingsClient mSettingsClient;
    private Marker markerCurrentLocation;
    private Marker firstMarker;
    private FusedLocationProviderClient mFusedLocationClient;
    private ArrayList<Double> pm10CurrentlyListDouble = new ArrayList<>();
    private ArrayList<Double> pm25CurrentlyListDouble = new ArrayList<>();
    private MenuItem itemTracking;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        getSupportActionBar().setDisplayShowTitleEnabled(false);


        String mCurrentLocation = getIntent().getStringExtra("mCurrentLocation");
        String stationsLocations = getIntent().getStringExtra("stationLocationArrayString");

        String pm10Currently = getIntent().getStringExtra("pm10Currently");
        String pm25Currently = getIntent().getStringExtra("pm25Currently");

        stationsLocations = clearString(stationsLocations);
        pm10Currently = clearString(pm10Currently);
        pm25Currently = clearString(pm25Currently);

        List<String> locationArray = Arrays.asList(mCurrentLocation.split(" "));
        List<String> stationsLocationArray = Arrays.asList(stationsLocations.split(" "));
        putLocationsIntoArray(stationsLocationArray);

        List<String> pm10CurrentlyListString = Arrays.asList(pm10Currently.split(" "));
        List<String> pm25CurrentlyListString = Arrays.asList(pm25Currently.split(" "));


        for (String item : pm10CurrentlyListString) {
            Double parsedItem = Double.parseDouble(item);
            pm10CurrentlyListDouble.add(parsedItem);

        }

        for (String item : pm25CurrentlyListString) {
            Double parsedItem = Double.parseDouble(item);
            pm25CurrentlyListDouble.add(parsedItem);

        }

        currLocation.setLatitude(Double.parseDouble(locationArray.get(0)));
        currLocation.setLongitude(Double.parseDouble(locationArray.get(1)));
        mSettingsClient = LocationServices.getSettingsClient(this);
        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);


        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);

        createLocationCallback();
        createLocationRequest();
        buildLocationSettingsRequest();

    }

    @Override
    protected void onStart() {
        super.onStart();

        createLocationRequest();
    }

    @Override
    public void onResume() {
        super.onResume();

        startLocationUpdates();
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        Double latitiude = currLocation.getLatitude();
        Double longitiude = currLocation.getLongitude();

        LatLng currPositionOnMap = new LatLng(latitiude, longitiude);
        firstMarker = mMap.addMarker(new MarkerOptions().position(currPositionOnMap).title("Moja pozycja"));
        firstMarker.setIcon(BitmapDescriptorFactory.fromResource(R.drawable.pin));
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(firstMarker.getPosition(), 15));
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return;
        }
        googleMap.setMyLocationEnabled(true);



        int iterator = 0;
        for (Location loc : stationsLocationsArray) {
            LatLng stationLatLng = new LatLng(loc.getLatitude(), loc.getLongitude());
            mMap.addMarker(new MarkerOptions().position(stationLatLng).title("Stacja pogodowa"));
            int radius = 1000;
            if (iterator == 1 || iterator==2)
                radius = 400;
            int color;
            if (pm10CurrentlyListDouble.get(iterator)>50 && pm10CurrentlyListDouble.get(iterator)>25) {
                color = 0x50b62e2e;
            }
            else if (pm10CurrentlyListDouble.get(iterator)<=50 && pm10CurrentlyListDouble.get(iterator)<=25){
                color = 0x508AD08D;
            }
            else {
                color = 0x50cccc00;
            }
            int strokeWidth = 1;
            mMap.addCircle(new CircleOptions()
                    .center(stationLatLng)
                    .radius(radius)
                    .fillColor(color))
                    .setStrokeWidth(strokeWidth);
            iterator++;

        }
    }


    private void putLocationsIntoArray(List<String> stationsArray) {
        for (int i = 0; i < stationsArray.size(); i++) {
            if (i % 2 == 1) {
                Double stationLatitude = Double.parseDouble(stationsArray.get(i - 1));
                Double stationLongitude = Double.parseDouble(stationsArray.get(i));
                Location locToArray = new Location("StationLocation");
                locToArray.setLatitude(stationLatitude);
                locToArray.setLongitude(stationLongitude);
                this.stationsLocationsArray.add(locToArray);
            }
        }

    }

    private void createLocationCallback() {
        mLocationCallback = new LocationCallback() {
            @Override
            public void onLocationResult(LocationResult locationResult) {
                super.onLocationResult(locationResult);

                currLocation = locationResult.getLastLocation();


                firstMarker.remove();

                if (markerCurrentLocation!= null) {
                    markerCurrentLocation.remove();
                }
                markerCurrentLocation =  mMap.addMarker(new MarkerOptions().position(new LatLng(currLocation.getLatitude(), currLocation.getLongitude())).title("Moja pozycja"));
                markerCurrentLocation.setIcon(BitmapDescriptorFactory.fromResource(R.drawable.pin));

                //<div>Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>
                 LatLng currPositionOnMap = new LatLng(currLocation.getLatitude(), currLocation.getLongitude());

                if (itemTracking.isChecked()) {
                    mMap.moveCamera(CameraUpdateFactory.newLatLng(currPositionOnMap));
                    mMap.animateCamera(CameraUpdateFactory.zoomTo(15));
                }

            }
        };
    }

    protected void createLocationRequest() {
        mLocationRequest = new LocationRequest();
        mLocationRequest.setInterval(10000);
        mLocationRequest.setFastestInterval(5000);
        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
    }

    private void buildLocationSettingsRequest() {
        LocationSettingsRequest.Builder builder = new LocationSettingsRequest.Builder();
        builder.addLocationRequest(mLocationRequest);
        mLocationSettingsRequest = builder.build();
    }

    private void startLocationUpdates() {

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            return;
        }
        mFusedLocationClient.requestLocationUpdates(mLocationRequest,
                mLocationCallback, Looper.myLooper());

    }

    private String clearString(String str){

        str = str.replace(",", "");
        str = str.replace("[", "");
        str = str.replace("]", "");
        return str;

    }

    public void goToLocation (View view) {

        int numberOfLocations = 1;
        EditText editText = (EditText) findViewById(R.id.WybierzLokacjeEditText);
        String loc = editText.getText().toString();
        Geocoder geocoder = new Geocoder(this);
        try {
            List<Address> addrList = geocoder.getFromLocationName(loc, numberOfLocations);
            if (addrList.size() == 0) {
                Toast.makeText(getApplicationContext(), "Zła lokacja", Toast.LENGTH_LONG).show();
            }

            else{
                Address placeWeMovedTo = addrList.get(0);
                double lat = placeWeMovedTo.getLatitude();
                double lon = placeWeMovedTo.getLongitude();
                LatLng newLatLngPosition = new LatLng(lat, lon);
                mMap.moveCamera(CameraUpdateFactory.newLatLng(newLatLngPosition));
                mMap.animateCamera(CameraUpdateFactory.zoomTo(15));
            }

            if (itemTracking.isChecked()) {
                itemTracking.setChecked(false);
                Toast.makeText(getApplicationContext(), "Wyłączam tryb śledzenia użytkownika", Toast.LENGTH_LONG).show();
            }



        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu){
        getMenuInflater().inflate(R.menu.map_menu, menu);
        itemTracking = menu.getItem(2);
        itemTracking.setCheckable(true);
        itemTracking.setOnMenuItemClickListener(new MenuItem.OnMenuItemClickListener() {
            @Override
            public boolean onMenuItemClick(MenuItem item) {
                if (item.isChecked()){
                    item.setChecked(false);
                    Toast.makeText(getApplicationContext(),"Wyłączam tryb śledzenia użytkownika",Toast.LENGTH_LONG).show();
                }
                else{
                    item.setChecked(true);
                    Toast.makeText(getApplicationContext(),"Włączam tryb śledzenia użytkownika",Toast.LENGTH_LONG).show();

                }

                return true;
            }
        });

        return super.onCreateOptionsMenu(menu);

    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item){
        switch (item.getItemId()){
            case R.id.normalMap:
                mMap.setMapType(GoogleMap.MAP_TYPE_NORMAL);
                break;
            case R.id.satteliteMap:
                mMap.setMapType(GoogleMap.MAP_TYPE_SATELLITE);
                break;
            default:
                break;
        }
        return true;
    }
}