package info.androidhive.appzan;

import java.util.ArrayList;
import java.util.Collections;

/**
 * Created by User on 2017-11-15.
 */

public class IndexReturner {

    public String returnIndex(ArrayList<Float> distTable){

        float minDistance = Collections.min(distTable);
        String index = null;

        for (int indexVal = 0; indexVal < distTable.size(); indexVal++) {
            if (distTable.get(indexVal) == minDistance) {
                index = Integer.toString(indexVal);
                break;
            }
        }
       return index;
    }
}
