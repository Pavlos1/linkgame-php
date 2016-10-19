<?php

$dbhost = 'localhost';
$dbuser = '';
$dbpass = '';

function getmysqli($db='') {
    global $dbhost, $dbuser, $dbpass;

    $mysqli = new mysqli($dbhost, $dbuser, $dbpass, $db);

    return $mysqli;
}
?>
