<?php
    include 'access.php';
    include 'dbfunc.php';
?>

<html>
<head>
<title>Tournament Results</title>
<script type="text/javascript">
    window.onload = function() {
        setInterval(function() {
            location.reload(true);
        }, 5000);
    };
</script>
</head>
<h1>Tournament results:</h1>
<p><a href="/">Back to home.</a></p>
<p>If you have JavaScript disabled, you may need to refresh the page repeatedly.</p>
<?php
    $res = getTournamentResults();
    if (!($res === "ok")) {
        print("<h3>$res</h3>");
        print("</html>");
        exit();
    }
?>
<table border="1">
    <tr>
        <td><h3>Rank</h3></td>
        <td><h3>UID</h3></td>
        <td><h3>Avg. Time / Placement (ms)</h3></td>
        <td><h3>No. of Placements Tested</h3></td>
        <?php
            $rank = 0;
            foreach ($ret as $entry) {
                ?>
                    <tr>
                        <td><p><?=$rank?></p></td>
                        <td><p><?=$entry[0]?></p></td>
                        <td><p><?=$entry[1]?></p></td>
                        <td><p><?=$entry[2]?></p></td>
                    </tr>
                <?php
            $rank++;
            }
        ?>
    </tr>
</table>
</html>
