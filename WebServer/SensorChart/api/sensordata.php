<?php
// Verzeichnis für die Raspberry Pi: /var/www/html/api/sensordata.php

// Header für JSON-Response
header('Content-Type: application/json');

// Datenbankverbindung Variablen
$ip = "10.10.75.98";
$port = 3306;
$user = "jgiera";
$password = "IBvm0-6BT7bxApKC";
$dbname = "WerteDB";

// Datenbankverbindung
$mysqli = new mysqli($ip, $user, $password, $dbname, $port);
if ($mysqli->connect_errno) {
    http_response_code(500);
    echo json_encode(array("error" => "Konnte nicht mit der Datenbank verbinden: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error));
    exit();
}

// Lese Parameter
$timeframe = isset($_GET['timeframe']) ? $_GET['timeframe'] : "Insgesamt";
$limitParam = isset($_GET['limit']) ? $_GET['limit'] : "Insgesamt";

$conditions = array();
if ($timeframe !== "Insgesamt") {
    // Berechne den unteren Grenzwert basierend auf Tagen
    $days = intval($timeframe);
    $lowerBound = date("Y-m-d 00:00:00", strtotime("-{$days} days"));
    $conditions[] = "datum >= '$lowerBound'";
}

$whereClause = "";
if (count($conditions) > 0) {
    $whereClause = "WHERE " . implode(" AND ", $conditions);
}

$limitClause = "";
if ($limitParam !== "Insgesamt" && is_numeric($limitParam)) {
    $limitClause = "LIMIT " . intval($limitParam);
}

// SQL-Abfrage unter Einbeziehung von WHERE und LIMIT
$sql = "SELECT datum, sensorName, Wert FROM messung $whereClause ORDER BY datum ASC $limitClause";
$result = $mysqli->query($sql);

// Daten sammeln
$data = [];
if ($result) {
    while($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
} else {
    http_response_code(500);
    echo json_encode(array("error" => "Fehler bei der Abfrage: " . $mysqli->error));
    exit();
}

// Ausgabe
echo json_encode($data);

// Verbindung schließen
$mysqli->close();
?>