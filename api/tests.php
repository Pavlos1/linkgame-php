<?php
    include '../session.php';
    include '../dbfunc.php';

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

    $ret = array();
    foreach ($rows[0] as $item) {
        if (is_int($item)) {
            array_push($ret, $item);
        } else {
            array_push($ret, htmlspecialchars($item));
        }
    }
    print(json_encode($ret));
