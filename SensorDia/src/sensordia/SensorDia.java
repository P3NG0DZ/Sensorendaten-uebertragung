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

public class SensorDia extends JFrame {
    private JComboBox<String> sensorComboBox;
    private JPanel chartPanelContainer;
    private JCheckBox showAllSensorsCheckBox;

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
            sensorComboBox.setSelectedIndex(0); // Automatisch die Daten des ersten Sensors auswählen
        }
    }

    private void plot() {
        boolean showAllSensors = showAllSensorsCheckBox.isSelected();
        DBverwaltung_MySQL dbVerwaltung = new DBverwaltung_MySQL("WerteDB");
        ArrayList<Messwert> messwerte = dbVerwaltung.getAlleMesswerte();

        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        for (Messwert messwert : messwerte) {
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
