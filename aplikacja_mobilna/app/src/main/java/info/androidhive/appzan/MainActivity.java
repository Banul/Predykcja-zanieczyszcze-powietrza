package info.androidhive.appzan;

import android.Manifest;
import android.app.FragmentTransaction;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentSender;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.Picture;
import android.location.Location;
import android.media.Image;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.Looper;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.design.widget.NavigationView;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import com.google.android.gms.common.api.ApiException;
import com.google.android.gms.common.api.ResolvableApiException;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.LocationSettingsRequest;
import com.google.android.gms.location.LocationSettingsResponse;
import com.google.android.gms.location.LocationSettingsStatusCodes;
import com.google.android.gms.location.SettingsClient;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Locale;
import java.util.Calendar;

import static android.R.attr.format;
import static android.R.attr.type;

/**
 * Implementując posłużyłem się m.in.:
 * https://stackoverflow.com/questions/37498167/listview-checkbox-repeated-every-4th-items
 * https://www.youtube.com/watch?v=YMJSBHAZsso
 * https://www.youtube.com/watch?v=_YF6ocdPaBg
 * https://www.youtube.com/watch?v=NHXa96-r8TY
 * https://www.youtube.com/watch?v=dr0zEmuDuIk
 * https://www.youtube.com/watch?v=J3R4b-KauuI
 * https://stackoverflow.com/questions/31233279/navigation-drawer-how-do-i-set-the-selected-item-at-startup
 * https://github.com/googlesamples/android-play-location/blob/master/LocationUpdates/app/src/main/java/com/google/android/gms/location/sample/locationupdates/MainActivity.java
 *
 *
 */

public class MainActivity extends AppCompatActivity implements DialogWindowEnableInternet.OnResultListener{

    private Context context = this;
    public static final int MY_PERMISSIONS_REQUEST_FINE_LOCATION = 99;
    private DrawerLayout mDrawerLayout;
    private ActionBarDrawerToggle mToggle;
    private ArrayList<ItemToList> listOfItems;
    private ArrayList<ItemToList> populatingList = new ArrayList<>();
    protected static final int REQUEST_CHECK_SETTINGS = 0x1;
    LocationRequest mLocationRequest;
    private FusedLocationProviderClient mFusedLocationClient;
    private LocationCallback mLocationCallback;
    private LocationSettingsRequest mLocationSettingsRequest;
    private SettingsClient mSettingsClient;
    private static final String TAG = MainActivity.class.getSimpleName();
    private Location mCurrentLocation;
    private boolean trackingFlag = true;
    private ProgressDialog mDialog;
    private boolean haveInternet;
    private Button showOnMap;
    private Button reactAppButton;
    private DistanceCounter distCounter;
    Calendar calendar = Calendar.getInstance();
    Date currentTime;





    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
        String dateNowString = sdf.format(calendar.getTime());
        DateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm");

        try {
             currentTime = format.parse(dateNowString);
        } catch (ParseException e) {
            e.printStackTrace();
        }


        setContentView(R.layout.activity_main);

        mDrawerLayout = (DrawerLayout) findViewById(R.id.drawerLayout);
        mToggle = new ActionBarDrawerToggle(this, mDrawerLayout, R.string.open, R.string.close);

        mDrawerLayout.addDrawerListener(mToggle);
        mToggle.syncState();
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);
        mSettingsClient = LocationServices.getSettingsClient(this);
        mDialog = ProgressDialog.show(this, "", "Prosze czekac na wczytanie sie aplikacji", true);
        final TextView stationText = (TextView) findViewById(R.id.StationText);
        stationText.setText("Trwa ładowanie...");
        stationText.setTextColor(Color.RED);
        stationText.setTextSize(25);
        haveInternet = haveNetworkConnection();
        if (!haveInternet)
        {
            FragmentTransaction ft = getFragmentManager().beginTransaction();
            DialogWindowEnableInternet dialog = new DialogWindowEnableInternet(this);
            dialog.setCancelable(false);
            dialog.show(ft,"dialogInternet");

        }

        else
        {
            FetchData fetchData = new FetchData(context, new CallbackFromAsync() {
                @Override
                public void change(ArrayList response) {

                    listOfItems = response;
                }
            }


            );

            fetchData.execute();
        }

        mDialog.show();

        final NavigationView navigation = (NavigationView)findViewById(R.id.navigation);

        navigation.setNavigationItemSelectedListener(
                new NavigationView.OnNavigationItemSelectedListener() {
                    @Override
                    public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                        trackingFlag = false;
                        SublistReturner returner = new SublistReturner();
                        switch(item.getItemId())
                        {
                            case (R.id.station1):
                                populatingList = returner.returnSublist(listOfItems, "1");
                                stationText.setText("Wybrana stacja : Wokalna");
                                stationText.setTextColor(Color.BLACK);
                                stationText.setTextSize(12);
                                mDrawerLayout.closeDrawer(Gravity.LEFT);
                                break;

                            case (R.id.station2):
                                populatingList = returner.returnSublist(listOfItems, "2");
                                stationText.setText("Wybrana stacja : Marszałkowska");
                                stationText.setTextColor(Color.BLACK);
                                stationText.setTextSize(12);
                                mDrawerLayout.closeDrawer(Gravity.LEFT);
                                break;

                            case  (R.id.station3):
                                populatingList = returner.returnSublist(listOfItems, "3");
                                stationText.setText("Wybrana stacja : Aleja Niepodległości");
                                stationText.setTextColor(Color.BLACK);
                                stationText.setTextSize(12);
                                mDrawerLayout.closeDrawer(Gravity.LEFT);
                                break;

                            case (R.id.station4):
                                populatingList = returner.returnSublist(listOfItems, "4");
                                stationText.setText("Wybrana stacja : Wierzejewskiego");
                                stationText.setTextColor(Color.BLACK);
                                stationText.setTextSize(12);
                                mDrawerLayout.closeDrawer(Gravity.LEFT);
                                break;

                            case (R.id.station5):
                                populatingList = returner.returnSublist(listOfItems, "5");
                                stationText.setText("Wybrana stacja : Brzozowa");
                                stationText.setTextColor(Color.BLACK);
                                stationText.setTextSize(12);
                                mDrawerLayout.closeDrawer(Gravity.LEFT);
                                break;

                            // stacja najblizsza mnie!
                            case (R.id.station6):
                                ArrayList<Float> distTable = distCounter.getDistancesArray(mCurrentLocation);
                                IndexReturner indexReturner = new IndexReturner();
                                String indexForData = indexReturner.returnIndex(distTable);
                                int indexForDataInt = Integer.parseInt(indexForData);
                                int indexForStatName = indexForDataInt;
                                String indexForStatNameString = String.valueOf(indexForStatName);
                                indexForData = String.valueOf(indexForDataInt+1);
                                populatingList = returner.returnSublist(listOfItems, indexForData);
                                stationText.setText(StationNameReturner.returnStationName(indexForStatNameString));
                                stationText.setTextSize(12);
                                mDrawerLayout.closeDrawer(Gravity.LEFT);
                                break;
                        }


                        populateListView();
                        return true;
                    }
                }
        );



        createLocationCallback();
        createLocationRequest();
        buildLocationSettingsRequest();


    }

    @Override
    protected void onStart() {
        super.onStart();

    }

    @Override
    public void onResume() {
        Log.d("onResume", "onResume");
        super.onResume();


        // sprawdzanie zezwolenia na uslugi, wziete z:
        // https://developer.android.com/training/permissions/requesting.html

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {

            if (ActivityCompat.shouldShowRequestPermissionRationale(this,
                    Manifest.permission.READ_CONTACTS)) {

            } else {

                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                        MY_PERMISSIONS_REQUEST_FINE_LOCATION);

            }


        }
        else {
            startLocationUpdates();
        }

    }

    // sprawdzanie zezwolenia na usługi
    // wzięte z : https://developer.android.com/training/permissions/requesting.html
    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           String permissions[], int[] grantResults) {
        switch (requestCode) {
            case MY_PERMISSIONS_REQUEST_FINE_LOCATION: {
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {

                } else {

                }
                return;
            }

        }
    }

    protected void onPause() {
        super.onPause();
        stopLocationUpdates();
    }

    private void buildLocationSettingsRequest() {
        LocationSettingsRequest.Builder builder = new LocationSettingsRequest.Builder();
        builder.addLocationRequest(mLocationRequest);
        mLocationSettingsRequest = builder.build();
    }

    // https://github.com/googlesamples/android-play-location/blob/master/LocationUpdates/app/src/main/java/com/google/android/gms/location/sample/locationupdates/MainActivity.java

    private void stopLocationUpdates() {
        mFusedLocationClient.removeLocationUpdates(mLocationCallback);
    }

    //  https://github.com/googlesamples/android-play-location/blob/master/LocationUpdates/app/src/main/java/com/google/android/gms/location/sample/locationupdates/MainActivity.java

    private void createLocationCallback() {
        mLocationCallback = new LocationCallback() {
            @Override
            public void onLocationResult(LocationResult locationResult) {
                super.onLocationResult(locationResult);

                mCurrentLocation = locationResult.getLastLocation();
                distCounter = new DistanceCounter();
                distCounter.setArray();
                ArrayList<Float> distTable = distCounter.getDistancesArray(mCurrentLocation);

                TextView wokalnaTextView = (TextView) findViewById(R.id.WokalnaVal);
                TextView marszalkowskaTexView = (TextView) findViewById(R.id.MarszalkowskaVal);
                TextView niepodleglosciTextView = (TextView) findViewById(R.id.NiepodleglosciVal);
                TextView wierzejewskiegoTextView = (TextView) findViewById(R.id.WierzejewskiegoVal);
                TextView brzozowaTextView = (TextView) findViewById(R.id.BrzozowaVal);

                String valWokalna = String.valueOf(distTable.get(0));
                double doubleDistance = Double.parseDouble(valWokalna);
                doubleDistance = doubleDistance/1000;
                valWokalna = String.format(Locale.ROOT,"%.2f", doubleDistance);
                wokalnaTextView.setText(valWokalna);

                String valMarszalkowska = String.valueOf(distTable.get(1));
                doubleDistance = Double.parseDouble(valMarszalkowska);
                doubleDistance = doubleDistance/1000;
                valMarszalkowska = String.format(Locale.ROOT,"%.2f", doubleDistance);
                marszalkowskaTexView.setText(valMarszalkowska);

                String valNiepodleglosci = String.valueOf(distTable.get(2));
                doubleDistance = Double.parseDouble(valNiepodleglosci);
                doubleDistance = doubleDistance/1000;
                valNiepodleglosci = String.format(Locale.ROOT,"%.2f", doubleDistance);
                niepodleglosciTextView.setText(valNiepodleglosci);

                String valWierzejewskiego = String.valueOf(distTable.get(3));
                doubleDistance = Double.parseDouble(valWierzejewskiego);
                doubleDistance = doubleDistance/1000;
                valWierzejewskiego = String.format(Locale.ROOT,"%.2f", doubleDistance);
                wierzejewskiegoTextView.setText(valWierzejewskiego);

                String valBrzozowa = String.valueOf(distTable.get(4));
                doubleDistance = Double.parseDouble(valBrzozowa);
                doubleDistance = doubleDistance/1000;
                valBrzozowa = String.format(Locale.ROOT,"%.2f", doubleDistance);
                brzozowaTextView.setText(valBrzozowa);

                if(trackingFlag) {
                    IndexReturner indexReturner = new IndexReturner();
                   String index = indexReturner.returnIndex(distTable);

                    if (index != null) {
                        TextView stationText = (TextView) findViewById(R.id.StationText);
                        SublistReturner returner = new SublistReturner();
                        if (listOfItems!=null && listOfItems.size()!=0) {
                            int indexForList = Integer.parseInt(index)+1;
                            populatingList = returner.returnSublist(listOfItems, String.valueOf(indexForList));
                            String textStat =  StationNameReturner.returnStationName(index);
                            stationText.setText(textStat);
                            stationText.setTextColor(Color.BLACK);
                            stationText.setTextSize(12);


                            populateListView();
                            trackingFlag = false;
                        }
                    }
                }
            }
        };
    }

    // wzięte częściowo z :
    // https://github.com/googlesamples/android-play-location/blob/master/LocationUpdates/app/src/main/java/com/google/android/gms/location/sample/locationupdates/MainActivity.java
    private void startLocationUpdates() {

        mSettingsClient.checkLocationSettings(mLocationSettingsRequest)
                .addOnSuccessListener(this, new OnSuccessListener<LocationSettingsResponse>() {
                    @Override
                    public void onSuccess(LocationSettingsResponse locationSettingsResponse) {
                        showOnMap = (Button) findViewById(R.id.pokazNaMapieButon);
                        reactAppButton = (Button) findViewById(R.id.reactAppButton);

                        showOnMap.setOnClickListener(new Button.OnClickListener() {
                            @Override
                            public void onClick(View v) {
                                LocationToStringConverter locConv = new LocationToStringConverter();
                                ArrayList<Location> locationsArray = distCounter.getLocations();
                                ArrayList<LocationModel> arrayListModel = locConv.convertArrayToString(locationsArray);

                                LocationModel locationModel = locConv.convertToString(mCurrentLocation);
                                CurrentPollutionReturner pollutionReturner= new CurrentPollutionReturner();

                                ArrayList<Double> pm10Currently = pollutionReturner.returnPm10(listOfItems);
                                ArrayList<Double> pm25Currently = pollutionReturner.returnPm25(listOfItems);

                                Intent intent = new Intent(getBaseContext(), MapsActivity.class);
                                intent.putExtra("mCurrentLocation", locationModel.toString());
                                intent.putExtra("stationLocationArrayString",arrayListModel.toString());
                                intent.putExtra("pm10Currently",pm10Currently.toString());
                                intent.putExtra("pm25Currently",pm25Currently.toString());
                                startActivity(intent);
                            }
                        });

                        reactAppButton.setOnClickListener(new Button.OnClickListener(){
                            @Override
                            public void onClick(View v) {
                                String url = "http://banul.com.s3-website.eu-central-1.amazonaws.com";
                                Intent i = new Intent(Intent.ACTION_VIEW);
                                i.setData(Uri.parse(url));
                                startActivity(i);
                            }
                        });

                        Log.i(TAG, "All location settings are satisfied.");

                        //noinspection MissingPermission
                        mFusedLocationClient.requestLocationUpdates(mLocationRequest,
                                mLocationCallback, Looper.myLooper());


                    }
                })
                .addOnFailureListener(this, new OnFailureListener() {
                    @Override
                    public void onFailure(@NonNull Exception e) {
                        int statusCode = ((ApiException) e).getStatusCode();
                        switch (statusCode) {
                            case LocationSettingsStatusCodes.RESOLUTION_REQUIRED:

                                try {
                                    ResolvableApiException rae = (ResolvableApiException) e;
                                    rae.startResolutionForResult(MainActivity.this, REQUEST_CHECK_SETTINGS);
                                } catch (IntentSender.SendIntentException sie) {
                                }
                                break;
                            case LocationSettingsStatusCodes.SETTINGS_CHANGE_UNAVAILABLE:
                                String errorMessage = "Blad!";
                                Toast.makeText(MainActivity.this, errorMessage, Toast.LENGTH_LONG).show();
                        }

                    }
                });


    }

    // wziete tez czesciowo z:
    //https:github.com/googlesamples/android-play-location/blob/master/LocationUpdates/app/src/main/java/com/google/android/gms/location/sample/locationupdates/MainActivity.java
    protected void createLocationRequest() {
        mLocationRequest = new LocationRequest();
        mLocationRequest.setInterval(10000);
        mLocationRequest.setFastestInterval(5000);
        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
        }


    @Override
    public boolean onOptionsItemSelected (MenuItem item){

        if (mToggle.onOptionsItemSelected(item)) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private void populateListView()
    {
        if (mDialog.isShowing())
            mDialog.dismiss();
        ArrayAdapter<ItemToList> adapter = new MyListAdapter();
        ListView list = (ListView) findViewById(R.id.listView);
        list.setAdapter(adapter);

    }

    @Override
    public void onCompleteFun(ArrayList<ItemToList> itemsList) {
        this.listOfItems = itemsList;

        if (listOfItems == null || listOfItems.size() == 0)
        {
            AlertDialog.Builder builder1 = new AlertDialog.Builder(context);
            builder1.setMessage("Proszę o włączenie Internetu - z powodu braku dostępu do sieci aplikacja zostanie wyłączona.");

            builder1.setPositiveButton(
                    "OK",
                    new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int id) {
                            dialog.cancel();
                            MainActivity.this.finishAndRemoveTask();
                            System.exit(0);
                        }
                    });
            AlertDialog alert11 = builder1.create();
            alert11.show();
        }
        populateListView();

    }

    ///////////////////////////////////////////////////////////////////////////////////////////////////

    private class MyListAdapter extends ArrayAdapter<ItemToList> {

        MyListAdapter() {
            super(MainActivity.this, R.layout.row_layout, populatingList);

        }
        @NonNull
        @Override
        // generuje wiersz listy
        // wzorowalem sie na:
        // https://stackoverflow.com/questions/10120119/how-does-the-getview-method-work-when-creating-your-own-custom-adapter
        public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
            //Upewniamy sie że mamy widok
            View itemView = convertView;
            if (itemView == null) {
                // zrenderuj widok
                itemView = getLayoutInflater().inflate(R.layout.row_layout, parent, false);

            }

            for (int i = 1; i< populatingList.size(); i++){
               String itemDateString = populatingList.get(i).getDate();
                SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm");
                Date itemDateDat = new Date();

                try {
                    itemDateDat = dateFormat.parse(itemDateString);

                } catch (ParseException e) {
                    e.printStackTrace();
                }


                // zeby pasowała data
                Calendar cal = Calendar.getInstance();
                cal.setTime(itemDateDat);
                cal.add(Calendar.HOUR_OF_DAY, 1);

                if (currentTime.before( cal.getTime())){
                    populatingList.get(i).setText("(predykcja)");
                }
            }

            TextView PM10 = (TextView) itemView.findViewById(R.id.PM10Val);
            String strPM10 = populatingList.get(position).getPm10();
            PM10.setText(strPM10);

            TextView prediction = (TextView) itemView.findViewById(R.id.predykcjaText);
            prediction.setTextColor(Color.RED);
            String pred = populatingList.get(position).getText();
            prediction.setText(pred);

            TextView date = (TextView) itemView.findViewById(R.id.DateVal);
            String strDate = populatingList.get(position).getDate();
            strDate = strDate.substring(0,16);
            date.setText(strDate);

            TextView PM25 = (TextView) itemView.findViewById(R.id.PM25Val);
            String strPM25 = populatingList.get(position).getPm25();
            PM25.setText(strPM25);

            TextView temperature = (TextView) itemView.findViewById(R.id.TemperaturaVal);
            String strTemp = populatingList.get(position).getTemperature();
            double doubleTemp = Double.parseDouble(strTemp);
            strTemp = String.format(Locale.ROOT, "%.1f", doubleTemp);
            temperature.setText(strTemp);

            TextView cisnienie = (TextView) itemView.findViewById(R.id.CisnienieVal);
            String strCisn = populatingList.get(position).getPressure();
            cisnienie.setText(strCisn);

            TextView silaWiatru = (TextView) itemView.findViewById(R.id.SilaVal);
            String strSil = populatingList.get(position).getWindStrength();
            double doubleSila = Double.parseDouble(strSil);
            strSil = String.format(Locale.ROOT, "%.1f", doubleSila);
            silaWiatru.setText(strSil);

            ImageView imagePm10 = (ImageView) itemView.findViewById(R.id.pm10Image);
            ImageView imagePm25 = (ImageView) itemView.findViewById(R.id.pm25Image);

            TextView PM10proc = (TextView) itemView.findViewById(R.id.CoStanowiVal);
            double pm10Double = Double.parseDouble(String.valueOf(strPM10));
            double coStanowiVal = pm10Double / 50;
            coStanowiVal = coStanowiVal * 100;
            String coStanowiValString = String.format("%.1f", coStanowiVal);
            PM10proc.setText(coStanowiValString);
            if (coStanowiVal <= 100) {
                PM10proc.setTextColor(Color.rgb(28, 140, 108));
                imagePm10.setImageResource(R.drawable.dobrepowietrze);
            } else {
                imagePm10.setImageResource(R.drawable.zlepowietrze);
                PM10proc.setTextColor(Color.rgb(152, 1, 0));
            }

            TextView PM25proc = (TextView) itemView.findViewById(R.id.CoStanowiVal2);
            double pm25Double = Double.parseDouble(String.valueOf(strPM25));
            double coStanowiVal2 = pm25Double / 25;
            coStanowiVal2 = coStanowiVal2 * 100;
            String coStanowiValString2 = String.format("%.1f", coStanowiVal2);
            PM25proc.setText(coStanowiValString2);
            if (coStanowiVal2 <= 100){
                PM25proc.setTextColor(Color.rgb(28, 140, 108));
            imagePm25.setImageResource(R.drawable.dobrepowietrze);
           }
            else{
                PM25proc.setTextColor(Color.rgb(152, 1, 0));
                imagePm25.setImageResource(R.drawable.zlepowietrze);
            }

            TextView pogoda = (TextView) itemView.findViewById(R.id.WarunkiVal);
            String strPogoda = populatingList.get(position).getWeatherCond();

            if (strPogoda.equals("Mostly Cloudy"))
            {
                strPogoda = "zachmurzenie";
            }

            else if (strPogoda.equals("Foggy"))
            {
                strPogoda = "mgliście";
            }

            else if (strPogoda.contains("Fog"))
            {
                strPogoda = "mgliście";
            }

            else if (strPogoda.equals("Light Rain"))
            {
                strPogoda = "deszcz";
            }

            else if (strPogoda.equals("Overcast"))
            {
                strPogoda = "pochmurno";
            }

            else if (strPogoda.equals("Cloudy"))
            {
                strPogoda = ("pochmurno");
            }

            else if (strPogoda.equals("Partly Cloudy"))
            {
                strPogoda = ("zachmurzenie");
            }
            else if (strPogoda.equals("Light Rain Showers"))
            {
                strPogoda = "niewielki deszcz";
            }

            else if (strPogoda.toLowerCase().contains("snow"))
            {
                strPogoda = "opady śniegu";
            }

            else if (strPogoda.toLowerCase().contains("clear"))
            {
                strPogoda = "czyste niebo";
            }

            else if (strPogoda.toLowerCase().contains("clouds"))
            {
                strPogoda = "pochmurnie";
            }
            else {
                strPogoda = "czyste niebo";
            }




            pogoda.setText(strPogoda);


            return itemView;

        }

    }

    // funkcja czesciowo wzieta z:
    // https://stackoverflow.com/questions/10863030/detecting-if-android-is-connected-to-internet
    private boolean haveNetworkConnection() {

        boolean haveInternetConnection = false;

        ConnectivityManager cm = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
        if (activeNetwork != null) { // connected to the internet
            if (activeNetwork.getType() == ConnectivityManager.TYPE_WIFI) {
                haveInternetConnection = true;
                Toast.makeText(context, activeNetwork.getTypeName()+" włączone, trwa ściąganie danych", Toast.LENGTH_SHORT).show();
            } else if (activeNetwork.getType() == ConnectivityManager.TYPE_MOBILE) {
                haveInternetConnection = true;
                Toast.makeText(context, activeNetwork.getTypeName() + " włącznone, trwa ściąganie danych", Toast.LENGTH_SHORT).show();
            }
        } else {

            Toast.makeText(context, "Internet jest wyłączony, proszę o włączenie", Toast.LENGTH_SHORT).show();
        }
        return haveInternetConnection;
    }


}
