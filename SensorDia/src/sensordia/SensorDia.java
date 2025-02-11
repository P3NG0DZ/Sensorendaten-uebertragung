package sensordia;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

public class SensorDia extends JFrame {
    private JComboBox<String> sensorComboBox;
    private JPanel chartPanelContainer;

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

        initComboBox();
    }

    private void initComboBox() {
        DBverwaltung_MySQL dbVerwaltung = new DBverwaltung_MySQL("WerteDB");
        ArrayList<Messwert> messwerte = dbVerwaltung.getAlleMesswerte();
        Set<String> sensorNames = new HashSet<>();
        for (Messwert messwert : messwerte) {
            sensorNames.add(messwert.getSensorName());
        }
        for (String sensorName : sensorNames) {
            sensorComboBox.addItem(sensorName);
        }
        if (sensorComboBox.getItemCount() > 0) {
            sensorComboBox.setSelectedIndex(0); // Automatically select the first sensor's data
        }
    }

    private void plot() {
        String sensorName = (String) sensorComboBox.getSelectedItem();
        DBverwaltung_MySQL dbVerwaltung = new DBverwaltung_MySQL("WerteDB");
        ArrayList<Messwert> messwerte = dbVerwaltung.getAlleMesswerte();

        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        for (Messwert messwert : messwerte) {
            if (messwert.getSensorName().equals(sensorName)) {
                dataset.addValue(messwert.getWert(), "Wert", messwert.getDatum());
            }
        }

        JFreeChart lineChart = ChartFactory.createLineChart(
                "Liniendiagramm für Sensor " + sensorName,
                "Datum",
                "Wert",
                dataset,
                PlotOrientation.VERTICAL,
                true, true, false);

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
