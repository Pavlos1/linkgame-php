<?php
session_name('linkgame_session_id');
    $secure = true;
    $httponly = true;
    ini_set('session-use_only_cookies', 1);
    ini_set("session.entropy_file", "/dev/urandom");
    ini_set("session.entropy_length", "512");

    $cookieParams = session_get_cookie_params();
    session_set_cookie_params($cookieParams["lifetime"],
        $cookieParams["path"],
        $cookieParams["domain"],
        $secure,
        $httponly);

    session_start();
    if (!isset($_SESSION['csrf'])) { $_SESSION['csrf'] = base64_encode( openssl_random_pseudo_bytes(32) ); }
?>
