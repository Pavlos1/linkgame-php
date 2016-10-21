<?php
    include '../session.php';
    include '../dbfunc.php';

    if ((!isset($_GET['csrf'])) || (!($_GET['csrf'] === $_SESSION['csrf']))) {
        error_log('CSRF verification failed, ' . $_SESSION['csrf'] . ' !== ' . $_GET['csrf']);
        print('[false]');
        exit();
    }

    if (!isset($_SESSION['uid'])) {
        error_log('Unauthorized access to test data');
        print('[false]');
        exit();
    }
    $uid = $_SESSION['uid'];

    $res = getTestData($uid);
    if (!($res === "ok")) {
        error_log($res);
        print('[false]');
        exit();
    }
    if (!isset($rows) || count($rows) === 0) {
        print('[false]');
        exit();
    }

    print(json_encode($rows[0]));
