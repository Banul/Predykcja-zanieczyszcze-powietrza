package info.androidhive.appzan;

import java.util.ArrayList;

/**
 * Created by User on 2017-11-12.
 */

public interface CallbackFromAsync <T> {

    void change(ArrayList<ItemToList> response);
}
