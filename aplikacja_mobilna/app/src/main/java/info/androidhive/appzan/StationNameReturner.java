package info.androidhive.appzan;

/**
 * Created by User on 2017-11-27.
 */

public class StationNameReturner {

    public static String returnStationName(String index){
        String textStat;
        switch (index)
        {
            case "0":
                textStat = "Wybrana najbliższa stacja : Wokalna";
                break;
            case "1":
                textStat = "Wybrana najbliższa stacja : Marszałkowska";
                break;
            case "2":
                textStat = "Wybrana najbliższa stacja : Aleja Niepodległości";
                break;
            case "3":
                textStat = "Wybrana najbliższa stacja : Wierzejewskiego";
                break;
            case "4":
                textStat = "Wybrana najbliższa stacja : Brzozowa";
                break;
            default:
                textStat = null;
        }

        return textStat;
    }
}
