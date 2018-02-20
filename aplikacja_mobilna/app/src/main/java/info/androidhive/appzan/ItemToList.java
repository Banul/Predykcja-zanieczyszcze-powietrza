package info.androidhive.appzan;



public class ItemToList {

    private String date;
    private String pressure;
    private String windStrength;
    private String temperature;
    private String pm10;
    private String pm25;
    private String weatherCond;
    private String stationId;
    private String text;

    ItemToList(String date, String pressure, String windStrength, String temperature, String weatherCond, String pm10, String pm25, String stationId) {
        this.date = date;
        this.pressure = pressure;
        this.windStrength = windStrength;
        this.temperature = temperature;
        this.pm10 = pm10;
        this.pm25 = pm25;
        this.weatherCond = weatherCond;
        this.stationId = stationId;
    }

    public String getStationId() {
        return stationId;
    }

    public void setStationId(String stationId) {
        this.stationId = stationId;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getPressure() {
        return pressure;
    }

    public void setPressure(String pressure) {
        this.pressure = pressure;
    }

    public String getWindStrength() {
        return windStrength;
    }

    public void setWindStrength(String windStrength) {
        this.windStrength = windStrength;
    }

    public String getTemperature() {
        return temperature;
    }

    public void setTemperature(String temperature) {
        this.temperature = temperature;
    }

    public String getPm10() {
        return pm10;
    }

    public void setPm10(String pm10) {
        this.pm10 = pm10;
    }

    public String getPm25() {
        return pm25;
    }

    public void setPm25(String pm25) {
        this.pm25 = pm25;
    }

    public String getWeatherCond() {
        return weatherCond;
    }

    public void setWeatherCond(String weatherCond) {
        this.weatherCond = weatherCond;
    }


    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

}