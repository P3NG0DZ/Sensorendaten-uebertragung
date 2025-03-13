package sensordia;

//Jfreechart importieren
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.renderer.category.LineAndShapeRenderer;
import org.jfree.data.category.DefaultCategoryDataset;
import org.jfree.chart.axis.CategoryAxis;
import org.jfree.chart.axis.CategoryLabelPositions;

//Restliche Imports
import javax.swing.*;
import java.awt.*;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.text.SimpleDateFormat; // Neuer Import: SimpleDateFormat für Datumskonvertierung
import java.text.ParseException;    // Neuer Import: ParseException abfangen
import java.util.Calendar;          // Neuer Import: zum Berechnen von Datumgrenzen
import java.util.Date;              // Neuer Import: Arbeiten mit Datum

public class SensorDia extends JFrame {
    private JComboBox<String> sensorComboBox;
    private JPanel chartPanelContainer;
    private JCheckBox showAllSensorsCheckBox;
    private Timer timer;
    private int lastCount = 0; // Zuletzt gezählte Anzahl an Messwerten
    private JComboBox<String> dateRangeComboBox; // Neuer ComboBox für den Zeitraum

    public SensorDia() {
        setTitle("Liniendiagramm");
        setSize(1400, 900);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        JPanel controlPanel = new JPanel();
        controlPanel.setLayout(new FlowLayout());

        sensorComboBox = new JComboBox<>();
        controlPanel.add(new JLabel("Sensor:"));
        controlPanel.add(sensorComboBox);
        
        // Neuer Code: Zeitraum ComboBox hinzufügen
        dateRangeComboBox = new JComboBox<>();
        dateRangeComboBox.addItem("Heute");
        dateRangeComboBox.addItem("Letzte 7 Tage");
        dateRangeComboBox.addItem("Letzte 30 Tage");
        dateRangeComboBox.addItem("Letzten Monate");
        dateRangeComboBox.addItem("Alle Anzeigen");
        controlPanel.add(new JLabel("Zeitraum:"));
        controlPanel.add(dateRangeComboBox);
        
        // Neuer Code: Listener zum Aktualisieren des Diagramms bei Änderung des Zeitraums
        dateRangeComboBox.addItemListener(new ItemListener() {
            @Override
            public void itemStateChanged(ItemEvent e) {
                if(e.getStateChange() == ItemEvent.SELECTED){
                    plot();
                }
            }
        });
        
        showAllSensorsCheckBox = new JCheckBox("Alle Sensoren anzeigen");
        controlPanel.add(showAllSensorsCheckBox);

        add(controlPanel, BorderLayout.NORTH);

        chartPanelContainer = new JPanel(new BorderLayout());
        add(chartPanelContainer, BorderLayout.CENTER);

        sensorComboBox.addItemListener(new ItemListener() {
            @Override
            public void itemStateChanged(ItemEvent e) {
                if (e.getStateChange() == ItemEvent.SELECTED) {
                    plot();
                }
            }
        });

        showAllSensorsCheckBox.addItemListener(new ItemListener() {
            @Override
            public void itemStateChanged(ItemEvent e) {
                plot();
            }
        });

        initComboBox();
        timer = new Timer(5000, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                checkForUpdates();
            }
        });

        timer = new Timer(5000, new ActionListener() { // Timer, der alle 5 Sekunden checkt, ob sich die Anzahl der Messwerte geändert hat
            @Override
            public void actionPerformed(ActionEvent e) {
                checkForUpdates();
            }
        });
        timer.start();
    }

    @Override
    public void dispose() { // Timer stoppen, wenn das Fenster geschlossen wird
        if (timer != null) {
            timer.stop();
        }
        super.dispose();
    }

    private void checkForUpdates() { // Checkt nach Aktualisierungen
        DBverwaltung_MySQL dbVerwaltung = new DBverwaltung_MySQL("WerteDB");

        int currenCount = dbVerwaltung.getAnzahlMesswerte();

        if (currenCount != lastCount) {
            lastCount = currenCount;
            String selectedSensor = (String) sensorComboBox.getSelectedItem(); // Aktuell ausgewählten Sensor speichern
            initComboBox();
            sensorComboBox.setSelectedItem(selectedSensor); // Gespeicherten Sensor wieder auswählen
            plot();
        } else {
            plot(); // Aktualisiere das Diagramm auch, wenn die Anzahl der Messwerte gleich bleibt
        }

    }

    private void initComboBox() {
        DBverwaltung_MySQL dbVerwaltung = new DBverwaltung_MySQL("WerteDB");
        ArrayList<Messwert> messwerte = dbVerwaltung.getAlleMesswerte();
        Set<String> sensorNames = new HashSet<>();
        for (Messwert messwert : messwerte) {
            sensorNames.add(messwert.getSensorName());
        }
        sensorComboBox.removeAllItems(); // Vor dem Hinzufügen von Items die ComboBox leeren
        for (String sensorName : sensorNames) {
            sensorComboBox.addItem(sensorName);
        }
        if (sensorComboBox.getItemCount() > 0 && sensorComboBox.getSelectedItem() == null) {
            sensorComboBox.setSelectedIndex(0); // Automatisch die Daten des ersten Sensors auswählen, wenn keiner ausgewählt ist
        }
    }

    private void plot() {
        boolean showAllSensors = showAllSensorsCheckBox.isSelected();
        DBverwaltung_MySQL dbVerwaltung = new DBverwaltung_MySQL("WerteDB");
        ArrayList<Messwert> messwerte = dbVerwaltung.getAlleMesswerte();
        
        // Neuer Code: Zeitfilter berechnen anhand der ComboBox Auswahl
        String selectedRange = (String) dateRangeComboBox.getSelectedItem();
        Date lowerBound = null;
        if (!"Alle Anzeigen".equals(selectedRange)) {
            Calendar cal = Calendar.getInstance();
            Date now = new Date();
            cal.setTime(now);
            switch (selectedRange) {
                case "Heute":
                    // Setzt die Uhrzeit auf 00:00:00
                    cal.set(Calendar.HOUR_OF_DAY, 0);
                    cal.set(Calendar.MINUTE, 0);
                    cal.set(Calendar.SECOND, 0);
                    cal.set(Calendar.MILLISECOND, 0);
                    break;
                case "Letzte 7 Tage":
                    cal.add(Calendar.DAY_OF_MONTH, -7);
                    break;
                case "Letzte 30 Tage":
                    cal.add(Calendar.DAY_OF_MONTH, -30);
                    break;
                case "Letzten Monate":
                    cal.add(Calendar.MONTH, -3); // Beispielsweise 3 Monate zurück
                    break;
                default:
                    break;
            }
            lowerBound = cal.getTime();
        }
        
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        
        for (Messwert messwert : messwerte) {
            // Neuer Code: Filterung nach Datum, falls nötig
            if (lowerBound != null) {
                try {
                    Date messwertDatum = sdf.parse(messwert.getDatum());
                    if(messwertDatum.before(lowerBound)){
                        continue; // Überspringe den Messwert, wenn er älter ist als die Grenze
                    }
                } catch (ParseException ex) {
                    ex.printStackTrace();
                    continue;
                }
            }
            if (showAllSensors || messwert.getSensorName().equals(sensorComboBox.getSelectedItem())) {
                dataset.addValue(messwert.getWert(), messwert.getSensorName(), messwert.getDatum());
            }
        }

        JFreeChart lineChart = ChartFactory.createLineChart(
                showAllSensors ? "Liniendiagramm für alle Sensoren" : "Liniendiagramm für Sensor " + sensorComboBox.getSelectedItem(),
                "Datum",
                "Wert",
                dataset,
                PlotOrientation.VERTICAL,
                true, true, false);

        if (!showAllSensors) {
            LineAndShapeRenderer renderer = new LineAndShapeRenderer();
            renderer.setSeriesShapesVisible(0, true);
            renderer.setSeriesShape(0, new java.awt.geom.Ellipse2D.Double(-3, -3, 6, 6));
            renderer.setSeriesLinesVisible(0, true);
            lineChart.getCategoryPlot().setRenderer(renderer);
        }

        CategoryAxis domainAxis = lineChart.getCategoryPlot().getDomainAxis();
        domainAxis.setCategoryLabelPositions(CategoryLabelPositions.UP_45);
        domainAxis.setTickLabelFont(new Font("Dialog", Font.PLAIN, 8));

        ChartPanel chartPanel = new ChartPanel(lineChart);
        chartPanel.setPreferredSize(new Dimension(1400, 800));
        chartPanelContainer.removeAll();
        chartPanelContainer.add(chartPanel, BorderLayout.CENTER);
        chartPanelContainer.revalidate();
        chartPanelContainer.repaint();
    }

    public static void main(String[] args) {
        EventQueue.invokeLater(new Runnable() {
            @Override
            public void run() {
                SensorDia frame = new SensorDia();
                frame.setVisible(true);
            }
        });
    }
}
