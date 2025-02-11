/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sensordia;

/**
 *
 * @author JCSBK-User
 */
public class Messwert { //Setter und Getter Methoden für die Klasse Messwert
    
    
    private String sensorName;
    private double wert;
    private String datum;
    private int id;
   
  

    
    //Hauptkonstruktur mit dem ich Arbeite für Setter und Getter Methoden erstelle
    public Messwert(int id, String sensorName, double wert, String datum) {
        this.sensorName = sensorName;
        this.wert = wert;
        this.datum = datum;
        this.id = id;
    }

    //Weiterer Konstruktor ohne die ID
    public Messwert(String sensorName, double wert, String datum) {
        this.sensorName = sensorName;
        this.wert = wert;
        this.datum = datum;
    }

    //Getter Methoden
    public String getSensorName() {
        return sensorName;
    }

    public double getWert() {
        return wert;
    }

    public String getDatum() {
        return datum;
    }

    public int getID() {
        return id;
    }

    //Setter Methoden
    public void setSensorName(String sensorName) {
        this.sensorName = sensorName;
    }

    public void setWert(double wert) {
        this.wert = wert;
    }

    public void setDatum(String datum) {
        this.datum = datum;
    }

    //toString Methode
    @Override
    public String toString() {
        return "Messwert{" + "sensorName=" + sensorName + ", wert=" + wert + ", datum=" + datum + ", id=" + id + '}';
    }

}







