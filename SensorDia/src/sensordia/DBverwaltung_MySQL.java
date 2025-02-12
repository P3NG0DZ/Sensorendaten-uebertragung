package sensordia;

import java.sql.*;
import java.util.*;


//SQL Tabelle von Messung:
//id, datum, sensorName, Wert


public class DBverwaltung_MySQL {
    DBZugriff_MySQL db;

    public DBverwaltung_MySQL(String datenbank) {
        db = new DBZugriff_MySQL(datenbank);
    }

    public int getNextSensorID() {
        int nextID = 1;
        ResultSet rs = null;
        try {
            String sql = "SELECT MAX(id) AS max_id FROM messung;";
            rs = db.lesen(sql);
            if (rs.next()) {
                nextID = rs.getInt("max_id") + 1;
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            if (rs != null) {
                try {
                    rs.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }
        return nextID;
    }

    public String speichern(Messwert einMesswert) {
        String sql = "INSERT INTO messung (sensorName, wert, datum) VALUES ('"
                + einMesswert.getSensorName() + "', "
                + einMesswert.getWert() + ", '"
                + einMesswert.getDatum() + "');";
        System.out.println(sql);
        return db.aendern(sql);
    }

    public String loeschen(Messwert einMesswert) {
        String sql = "DELETE FROM messung WHERE id = '"
                + einMesswert.getID() + "';";
        System.out.println(sql);
        return db.aendern(sql);
    }

    public ArrayList<Messwert> getAlleMesswerte() {
        ArrayList<Messwert> messwerte = new ArrayList<Messwert>();
        ResultSet rs = null;
        try {
            String sql = "SELECT * FROM messung;";
            System.out.println(sql);
            rs = db.lesen(sql);
            while (rs.next()) {
                Messwert einMesswert = new Messwert(rs.getInt("id"),
                        rs.getString("sensorName"),
                        rs.getDouble("wert"),
                        rs.getString("datum"));
                messwerte.add(einMesswert);
                System.out.println(einMesswert.toString());
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            if (rs != null) {
                try {
                    rs.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }
        return messwerte;
    }

    public String aendern(Messwert einMesswert) {
        String sql = "UPDATE messung SET "
                + "sensorName = '" + einMesswert.getSensorName() + "',"
                + "wert = '" + einMesswert.getWert() + "',"
                + "datum = '" + einMesswert.getDatum()
                + "' WHERE id = " + einMesswert.getID() + ";";
        System.out.println(sql);
        return db.aendern(sql);
    }


    public int getAnzahlMesswerte() { // Überprüft ob sich Daten in der Datenbank geändert haben
        int anzahl = 0;
        ResultSet rs = null;
        try {
            String sql = "SELECT COUNT(*) AS anzahl FROM messung;";
            rs = db.lesen(sql);
            if (rs.next()) {
                anzahl = rs.getInt("anzahl");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            if (rs != null) {
                try {
                    rs.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }
        return anzahl;


    }
}