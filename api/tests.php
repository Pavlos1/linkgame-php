<?php
    include '../session.php';
    include '../dbfunc.php';

    if ((!isset($_GET['csrf'])) || (!($_GET['csrf'] === $_SESSION['csrf']))) {
        print("[false]");
        exit();
    }

    if (!isset($_SESSION['uid'])) {
        print("[false]");
        exit();
    }
    $uid = $_SESSION['uid'];

    $res = getTestData($uid);
    if (!($res === "ok")) {
        print("[false]");
        exit();
    }
    if (!isset($rows) || count($rows) === 0) {
        print("[false]");
        exit();
    }

    print(json_encode($rows[0]));
