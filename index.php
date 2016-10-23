<?php
    include 'access.php';
    include 'dbfunc.php';
    // TODO: Make UI look less like total crap

    if (isset($_POST['submit']) && isset($_POST['what']) && $_POST['what'] === 'upload') {
        if ((!isset($_POST['csrf'])) || (!($_POST['csrf'] === $_SESSION['csrf']))) {
            ?>
                <html><h1>CSRF verification failed</h1></html>
            <?php
            exit();
        }
        $target_dir = '/srv/jars/';
        $target_file = $target_dir . $uid . '.jar';
        if (move_uploaded_file($_FILES['jar']['tmp_name'], $target_file)) {
            $msg = "File uploaded successfully. ";
            $res = doFileUpdate($uid);
            if (!($res === "ok")) { $msg = "$res"; }
        } else {
            $msg = "Something went wrong during file upload. ";
        }
    }
?>

<html>
    <head>
        <title>LinkGame Tournament</title>
        <script type="text/javascript">
            window.onload = function() {
                setInterval(function() {
                    var oReq = new XMLHttpRequest();
                    oReq.addEventListener("load", function() {
                        if (this.responseText != "[false]") {
                            var data = JSON.parse(this.responseText);
                            var div = document.getElementById("testresults");
                            div.innerHTML = "";

                            if (data[2] === 0) {
                                div.innerHTML += "<p>Tests are still queued/running.</p>";
                            } else if (data[2] === 1){
                                div.innerHTML += "<p>All tests passed. Your bot is now registered in the tournament.</p>";
                            } else {
                                div.innerHTML += "<p>Some tests failed. See debug log below:</p>";
                                if (data[3] === null) {
                                    div.innerHTML += "<p>No data.</p>";
                                } else {
                                    div.innerHTML += "<p>"
                                    for (var i=0; i<data[3].length; i++) {
                                        if (data[3][i] === '\n' || data[3][i] === '\r') {
                                            div.innerHTML += "</p><p>";
                                        } else {
                                            div.innerHTML += data[3][i];
                                        }
                                    }
                                    div.innerHTML += "</p>"
                                }
                            }
                        }
                    });
                    oReq.open("GET", "/api/tests.php");
                    oReq.send();
                }, 5000);
            };
        </script>
    </head>

    <h1>LinkGame Tournament - Home</h1>
    <?php if (isset($msg)) { print("<p>$msg</p>"); } ?>
    <p>You have successfully authenticated as <?=htmlspecialchars($uid)?>.
Please only make one submission per group.</p>
    <p><a href="/results.php">See tournament results.</a></p>
    <p>Upload JAR file:</p>
    <form method="post" action="/index.php" enctype="multipart/form-data">
        <input type="hidden" name="what" value="upload"/>
        <input type="hidden" name="csrf" value="<?=$_SESSION['csrf']?>"/>
        <input type="file" name="jar" id="jar"/>
        <input type="submit" value="Upload JAR" name="submit"/>
    </form>

    <br/>
    <br/>
    <p>Results appear below when they are available. If you have
JavaScript disabled, you may need to refresh the page repeatedly.</p>
    <p>Test results for uploaded JAR:</p>
    <div id="testresults">
<?php
    $res = getTestData($uid);
    if (!($res === "ok")) print("<p>$res</p>");
    else {
        if (count($rows) === 0) {
            print('<p>No file uploaded.</p>');
        } else {
            if ($rows[0][2] === 0) { print '<p>Tests are still queued/running.</p>'; }
            else if ($rows[0][2] === 1) { print '<p>All tests passed. Your bot is now registered in the tournament.</p>'; }
            else if ($rows[0][2] === -1) { 
                print '<p>Some tests failed. See debug log below:</p>';
                if (!($rows[0][3] === NULL)) {
                    foreach(preg_split("/((\r?\n)|(\r\n?))/", $rows[0][3]) as $line){
                        print("<p>" . htmlspecialchars($line) . "</p>");
                    }
                } 
            }
        }
    }
?>
    </div>
    <form method="post" action="/logout.php">
    <input type="hidden" name="csrf" value="<?=$_SESSION['csrf']?>"/>
    <input type="hidden" name="what" value="logout"/>
    <button type="submit">Logout</button>
    </form>
</html>
