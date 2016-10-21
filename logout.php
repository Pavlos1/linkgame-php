<?php
    // TODO: Make all this actually work
    session_start();
    if (!isset($_SESSION['csrf'])) { $_SESSION['csrf'] = base64_encode( openssl_random_pseudo_bytes(32) ); }

    if (isset($_POST['what']) && $_POST['what'] === 'logout') {
        if ((!isset($_POST['csrf'])) || (!($_POST['csrf'] === $_SESSION['csrf']))) {
            ?>
                <html><h1>CSRF verification failed</h1></html>
            <?php
                exit();
        }

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
