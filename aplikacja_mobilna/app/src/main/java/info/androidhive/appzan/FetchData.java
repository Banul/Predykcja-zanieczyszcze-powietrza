package info.androidhive.appzan;

import android.content.Context;
import android.os.AsyncTask;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

/*
* Do implementacji posłużyłem się stronami:
* https://stackoverflow.com/questions/2492076/android-reading-from-an-input-stream-efficiently
* https://stackoverflow.com/questions/14376807/how-to-read-write-string-from-a-file-in-android
* https://stackoverflow.com/questions/9671546/asynctask-android-example
* https://javastart.pl/static/narzedzia/asynctask/
* https://stackoverflow.com/questions/6697147/json-iterate-through-jsonarray
*
 */

public class FetchData extends AsyncTask <Void,Void,ArrayList<ItemToList>>{
    private Context mContext;
    private HttpURLConnection mUrlConnection;
    private ArrayList<ItemToList> items = new ArrayList<>();
    private CallbackFromAsync <List<ItemToList>> mCallback;



    FetchData(Context context, CallbackFromAsync callbackFromAsync)
    {
        this.mContext = context;
        this.mCallback = callbackFromAsync;

    }

    protected void onPreExecute()
    {

    }

    @Override
    protected ArrayList<ItemToList> doInBackground(Void... params) {

        try {
            URL url = new URL("http://inzyniercorazblizej.eu-central-1.elasticbeanstalk.com//currentDataAndPrediction");
            mUrlConnection = (HttpURLConnection) url.openConnection();
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(mUrlConnection.getInputStream()));
            StringBuilder stringBuilder = new StringBuilder();
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                stringBuilder.append(line).append("\n");
            }
            bufferedReader.close();
            String JsonString = stringBuilder.toString(); //obiekt który parsujemy metodą ParseJson
            ParseJson(JsonString);

            return items;

        } catch (IOException e) {
            e.printStackTrace();
            return null;
        } finally {
            mUrlConnection.disconnect();
        }
    }
        protected void onPostExecute(ArrayList<ItemToList> response) {
            if (response == null || response.size()==0) {
                Toast.makeText(mContext,"No Results",Toast.LENGTH_LONG).show();
            }
            if(mCallback!=null)
            {
                mCallback.change(response);
            }
        }

        private void ParseJson(String JsonString)
        {

            try
                {

                    JSONArray jsonArray = new JSONArray(JsonString);

                    int iterator = 0;

                    String pressure;
                    String windStrength;
                    String temperature;
                    String weatherCond;
                    String pm10;
                    String pm25;
                    String stationId;
                    String date;

                    while (iterator < jsonArray.length())
                    {
                        JSONObject JObject = jsonArray.getJSONObject(iterator);
                        pressure = JObject.getString("pressure");
                        windStrength = JObject.getString("windStrength");
                        temperature = JObject.getString("temperature");
                        weatherCond = JObject.getString("weatherCond");
                        pm10 = JObject.getString("pm10");
                        pm25 = JObject.getString("pm25");
                        date = JObject.getString("date");
                        JSONObject station = JObject.getJSONObject("stationModel");
                        stationId = station.getString("id");

                        items.add((new ItemToList(date,pressure,windStrength,temperature,weatherCond,pm10,pm25, stationId)));
                        iterator++;

                    }

                }

                catch (JSONException e) {
                e.printStackTrace();

            }
        }
  }
