package sensordia;

import java.sql.*;

public class DBZugriff_MySQL {
    Connection db;
    String mDB;
    Statement stmtSQL;
    String dbname;
    String user;
    String password;
    String ip;
    String port;
    private static boolean connectionMessageShown = false; // Wird auf true gesetzt, wenn die Verbindungsmeldung bereits angezeigt wurde

    public DBZugriff_MySQL(String datenbankname) {
        dbname = datenbankname;
        user = "jgiera";
        password = "IBvm0-6BT7bxApKC";
        ip = "10.10.75.98";
        port = "3306";
        oeffneDB();
        showConnectionMessage();
    }

    public DBZugriff_MySQL(String ip, String port, String datenbankname, String user, String password) {
        dbname = datenbankname;
        this.user = user;
        this.password = password;
        this.ip = ip;
        this.port = port;
        oeffneDB();
        showConnectionMessage();
    }

    public DBZugriff_MySQL(String datenbankname, String user, String password) {
        dbname = datenbankname;
        this.user = user;
        this.password = password;
        ip = "10.10.75.98";
        port = "3306";
        oeffneDB();
        showConnectionMessage();
    }

    public final void oeffneDB() {
        try {
            Class.forName("org.mariadb.jdbc.Driver");
            mDB = "jdbc:mariadb://" + ip + ":" + port + "/" + dbname;
            db = DriverManager.getConnection(mDB, user, password);
            stmtSQL = db.createStatement();
        } catch (ClassNotFoundException err) {
            System.err.println("Treiberklasse konnte nicht geladen werden!");
            err.printStackTrace();
        } catch (SQLException err) {
            System.err.println("Datenbank konnte nicht geoeffnet werden!");
            err.printStackTrace();
        }
    }

    private void showConnectionMessage() {
        if (!connectionMessageShown) {
            if (db != null) {
                System.out.println("Verbindung zur Datenbank erfolgreich hergestellt.");
            } else {
                System.err.println("Verbindung zur Datenbank fehlgeschlagen.");
            }
            connectionMessageShown = true;
        }
    }

    public ResultSet lesen(String pSQL) {
        ResultSet rs = null;
        try {
            rs = stmtSQL.executeQuery(pSQL);
        } catch (SQLException err) {
            System.err.println("Lesen fehlgeschlagen " + err.getMessage());
        }
        return rs;
    }

    public String aendern(String pSQL) {
        try {
            stmtSQL.executeUpdate(pSQL);
        } catch (SQLException err) {
            System.err.println("Aendern fehlgeschlagen " + err.getMessage());
            return err.getMessage();
        }
        return "Erfolgreich";
    }

    public void schliesseDB() {
        try {
            if (stmtSQL != null && !stmtSQL.isClosed()) {
                stmtSQL.close();
            }
            if (db != null && !db.isClosed()) {
                db.close();
            }
        } catch (SQLException err) {
            System.err.println("Schliessen fehlgeschlagen");
            err.printStackTrace();
        }
    }
}