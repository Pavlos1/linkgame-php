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
        return 'ok';
    }

    function getPlayersInTournament() {
        $mysqli = getmysqli('linkgame');
        if (! $mysqli) { return 'Database error: failed to open connection to MySQL'; }
        $stmt = $mysqli->prepare('SELECT uid FROM tests WHERE testStatus=1;');
        if (! $stmt) { return 'Database error: failed to prepare query'; }
        if (! $stmt->execute()) { return 'Database error: failed to execute query: ' . $stmt->error; }

        $rows = $stmt->get_result()->fetch_all();
        $stmt->close();

        global $players;
        $players = array();
        foreach ($rows as $value) {
            array_push($players, $value[0]);
        }

        return 'ok';
    }

    function getPlayerStats($uid) {
        $mysqli = getmysqli('linkgame');
        if (! $mysqli) { return NULL; }
        $stmt = $mysqli->prepare('SELECT timeTaken FROM tournament WHERE uid=?;');
        if (! $stmt) { return NULL; }
        if (! $stmt->bind_param('s', $uid)) { return NULL; }
        if (! $stmt->execute()) { return NULL; }

        $rows = $stmt->get_result()->fetch_all();
        if (count($rows) < 1) { return NULL; }

        $total = 0;
        foreach($rows as $value) {
           $total += $value[0];
        }
        return array(round($total / count($rows)), count($rows));
    }

    function tournamentCmp($a, $b) {
        return $a[1] - $b[1];
    }

    function getTournamentResults() {
        global $players;
        $res = getPlayersInTournament();
        if (! $res === "ok") { return $res; }

        global $ret;
        $ret = array();
        foreach($players as $uid) {
            $stat = getPlayerStats($uid);
            if (!($stat === NULL)) {
                array_push($ret, array($uid, $stat[0], $stat[1]));
            }
        }

        usort($ret, "tournamentCmp");

        return 'ok';
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

        return 'ok';
    }
?>
