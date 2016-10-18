<?php
    include 'access.php';

    if (isset($_POST['submit'])) {
        $target_dir = '/srv/jars/';
        $target_file = $target_dir . $uid . '.jar';
        if (move_uploaded_file($_FILES['jar']['jar'], $target_file)) {
            $msg = "File uploaded successfully.";
        } else {
            $msg = "Something went wrong during file upload."
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
        <input type="file" name="jar" id="jar">
        <input type="submit" value="Upload JAR" name="submit">
    </form>

    <br/>
    <br/>
    <p>Results appear below when they are available. If you have
JavaScript disabled, you may need to refresh the page.</p>
    <p>TODO: Implement</p> 
</html>
