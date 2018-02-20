package info.androidhive.appzan;

import android.app.Activity;
import android.app.Dialog;
import android.app.DialogFragment;
import android.content.Context;
import android.content.DialogInterface;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AlertDialog;

import java.util.ArrayList;

/**
    Korzystałem m.in. z:
 https://stackoverflow.com/questions/8818290/how-do-i-connect-to-a-specific-wi-fi-network-in-android-programmatically - wifi
 https://stackoverflow.com/questions/25075343/how-do-i-connect-to-multiple-wifi-networks-one-after-the-another-programatically - wifi
 https://stackoverflow.com/questions/32258125/onattachactivity-deprecated-where-i-can-check-if-the-activity-implements-call
 https://developer.android.com/guide/components/fragments.html


 */

public class DialogWindowEnableInternet extends DialogFragment{

    private Context mContext;
    private ArrayList<ItemToList> listOfItems;

    public interface OnResultListener
    {
        void onCompleteFun (ArrayList <ItemToList> itemsList);
    }

    private OnResultListener mListener;

    public DialogWindowEnableInternet(Context context){

        this.mContext = context;
    }

    @Override
    public void onAttach(Context context)
    {
        super.onAttach(context);
            super.onAttach(context);
            try {
                mListener = (OnResultListener) context;
            } catch (ClassCastException e) {
                throw new ClassCastException(context.toString() + " must implement interface!");

        }
        }

    @Override
    public void onAttach(Activity activity)
    {
        super.onAttach(activity);
            super.onAttach(activity);
                mListener = (OnResultListener) activity;


    }


        @Override
        public Dialog onCreateDialog(Bundle savedInstanceState) {
            AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
            builder.setMessage("Brak dostępu do Internetu. Czy spróbować włączyć Wi-Fi?")
                    .setPositiveButton("Tak", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int id) {
                            WifiManager wifiManager = (WifiManager)mContext.getSystemService(Context.WIFI_SERVICE);
                            wifiManager.setWifiEnabled(true);
                            Handler handler = new Handler();
                            handler.postDelayed(new Runnable() {
                                public void run() {

                                    FetchData fetchData = new FetchData(mContext, new CallbackFromAsync() {
                                        @Override
                                        public void change(ArrayList response) {

                                            listOfItems = response;
                                            mListener.onCompleteFun(listOfItems);


                                        }
                                    });

                                    fetchData.execute();
                                }
                            }, 4000);

                        }
                    })
                    .setNegativeButton("Nie", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int id) {

                            mListener.onCompleteFun(listOfItems);
                        }
                    })
                    .setCancelable(false);

            builder.setCancelable(false);
            return builder.create();
        }


}
