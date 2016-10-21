<?php
    // TODO: Make all this actually work
    session_start();

    if (isset($_POST['what']) && $_POST['what'] === 'logout') {
        session_unset();
        session_destroy();
?>
    <html>
        <h1>Logout Successful</h1>
        <p>To log back in, <a href="/">click here.</a></p>
    </html>
<?php } else { ?>
    <html>
        <h1>Nothing to see here.</h1>
    </html>
<?php } ?>
