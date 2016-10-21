<?php

include 'db.php';

function getTestData($uid) {
        $mysqli = getmysqli('linkgame');
        if (! $mysqli) { return 'Database error: failed to open connection to MySQL'; }
        $stmt = $mysqli->prepare('SELECT * FROM tests WHERE uid=?;');
        if (! $stmt) { return 'Database error: failed to prepare query'; }
        if (! $stmt->bind_param('s', $uid)) { return 'Database error: failed to bind uid'; }
        if (! $stmt->execute()) { return 'Database error: failed to execute query: ' . $stmt->error; }

        global $rows;
        $rows = $stmt->get_result()->fetch_all();
        $stmt->close();
        return "ok";
    }

    function doFileUpdate($uid) {
        $res = getTestData($uid);
        if (!($res === "ok")) return $res;
        global $rows;

        $mysqli = getmysqli('linkgame');
        if (! $mysqli) { return 'Database error: failed to open connection to MySQL'; }
        if (count($rows) === 0) {
            // Insert new entry
            $stmt = $mysqli->prepare('INSERT INTO tests SET uid=?, testStatus=0, debug=NULL');
            if (! $stmt) { return 'Database error: failed to prepare query'; }
            if (! $stmt->bind_param('s', $uid)) { return 'Database error: failed to bind uid'; }
            if (! $stmt->execute()) { return 'Database (insert) error: failed to execute query: ' . $stmt->error; }
            $stmt->close();
        } else {
            // Update existing entry
            $stmt = $mysqli->prepare('UPDATE tests SET testStatus=0, debug=NULL WHERE uid=?');
            if (! $stmt) { return 'Database error: failed to prepare query'; }
            if (! $stmt->bind_param('s', $uid)) { return 'Database error: failed to bind uid'; }
            if (! $stmt->execute()) { return 'Database (update) error: failed to execute query' . $stmt->error; }
            $stmt->close();
        }
        // Clear out the main tournament table
        $stmt = $mysqli->prepare('DELETE FROM tournament WHERE uid=?;');
        if (! $stmt) { return 'Database error: failed to prepare query'; }
        if (! $stmt->bind_param('s', $uid)) { return 'Database error: failed to bind uid'; }
        if (! $stmt->execute()) { return 'Database (delete) error: failed to execute query: ' . $stmt->error; }
        $stmt->close();

        return "ok";
    }
?>
