<?php
    include 'access.php';
    include 'db.php';

    function getTestData() {
        global $uid;

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

    function doFileUpdate() {
        $res = getTestData();
        if (!($res === "ok")) return $res;
        global $rows;
        global $uid;

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

        return "ok";
    }

    if (isset($_POST['submit']) && isset($_POST['what']) && $_POST['what'] === 'upload') {
        $target_dir = '/srv/jars/';
        $target_file = $target_dir . $uid . '.jar';
        if (move_uploaded_file($_FILES['jar']['tmp_name'], $target_file)) {
            $msg = "File uploaded successfully. ";
            $res = doFileUpdate();
            if (!($res === "ok")) { $msg = "$res"; }
        } else {
            $msg = "Something went wrong during file upload. ";
        }
    }
?>

<html>
    <h1>Welcome</h1>
    <?php if (isset($msg)) { print("<p>$msg</p>"); } ?>
    <p>You have successfully authenticated as <?=$uid?>.
Please only make one submission per group.</p>
    <p>Upload JAR file:</p>
    <form method="post" action="/index.php" enctype="multipart/form-data">
        <input type="hidden" name="what" value="upload"/>
        <input type="file" name="jar" id="jar"/>
        <input type="submit" value="Upload JAR" name="submit"/>
    </form>

    <br/>
    <br/>
    <p>Results appear below when they are available. If you have
JavaScript disabled, you may need to refresh the page repeatedly.</p>
    <p>Test results for uploaded JAR:</p>
<?php
    $res = getTestData();
    if (!($res === "ok")) print("<p>$res</p>");
    else {
        if (count($rows) === 0) {
            print('<p>No file uploaded.</p>');
        } else {
            if ($rows[0][2] === 0) { print '<p>Tests are still queued/running.</p>'; }
            else if ($rows[0][2] === 1) { print '<p>All tests passed. Your bot is now registered in the tournament.</p>'; }
            else if ($rows[0][2] === -1) { 
                print '<p>Some tests failed. See debug log below:</p>';
                if (!($rows[0][3] === NULL)) print("<p>$rows[0][2]</p>"); 
            }
        }
    }
?>
    <form method="post" action="/logout.php">
    <input type="hidden" name="what" value="logout"/>
    <button type="submit">Logout</button>
    </form>
    <p>TODO: Implement tournament</p> 
</html>
