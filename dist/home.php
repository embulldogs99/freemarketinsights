<?php
// We need to use sessions, so you should always start sessions using the below code.
session_start();
// If the user is not logged in redirect to the login page...
if (!isset($_SESSION['loggedin'])) {
	header('Location: index.html');
	exit();
}
?>

<!DOCTYPE html>
<html>

<head>
    <!-- Mobile Specific Meta -->
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Favicon-->
    <link rel="shortcut icon" href="img/fav.png">
    <!-- Author Meta -->
    <meta name="Marius Morar" content="">
    <!-- Meta Description -->
    <meta name="description" content="">
    <!-- Meta Keyword -->
    <meta name="keywords" content="">
    <!-- meta character set -->
    <meta charset="UTF-8">
    <!-- Site Title -->
    <title>Free Market Insights</title>
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.1/css/all.css">

    <style>
        .navtop {
            background-color: #2f3947;
            height: 60px;
            width: 100%;
            border: 0;
        }
        
        .navtop div {
            display: flex;
            margin: 0 auto;
            width: 1000px;
            height: 100%;
        }
        
        .navtop div h1,
        .navtop div a {
            display: inline-flex;
            align-items: center;
        }
        
        .navtop div h1 {
            flex: 1;
            font-size: 24px;
            padding: 0;
            margin: 0;
            color: #eaebed;
            font-weight: normal;
        }
        
        .navtop div a {
            padding: 0 20px;
            text-decoration: none;
            color: #c1c4c8;
            font-weight: bold;
        }
        
        .navtop div a i {
            padding: 2px 8px 0 0;
        }
        
        .navtop div a:hover {
            color: #eaebed;
        }
        
        body.loggedin {
            background-color: #f3f4f7;
        }
        
        .content {
            width: 1000px;
            margin: 0 auto;
        }
        
        .content h2 {
            margin: 0;
            padding: 25px 0;
            font-size: 22px;
            border-bottom: 1px solid #e0e0e3;
            color: #4a536e;
        }
        
        .content > p,
        .content > div {
            box-shadow: 0 0 5px 0 rgba(0, 0, 0, 0.1);
            margin: 25px 0;
            padding: 25px;
            background-color: #fff;
        }
        
        .content > p table td,
        .content > div table td {
            padding: 5px;
        }
        
        .content > p table td:first-child,
        .content > div table td:first-child {
            font-weight: bold;
            color: #4a536e;
            padding-right: 15px;
        }
        
        .content > div p {
            padding: 5px;
            margin: 0 0 10px 0;
        }
    </style>
</head>

<body class="loggedin">
    <nav class="navtop">
        <div>
            <h1>Free Market Insights</h1>
            <a href="profile.php"><i class="fas fa-user-circle"></i>Profile</a>
            <a href="logout.php"><i class="fas fa-sign-out-alt"></i>Logout</a>
        </div>
    </nav>
    <div class="content">
        <h2>Home Page</h2>
        <p>Welcome back,
            <?=$_SESSION['name']?>!</p>
    </div>
</body>

</html>