
<!DOCTYPE html>
<?php session_start(); ?>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Simple Sidebar - Start Bootstrap Template</title>

    <!-- Bootstrap Core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="css/simple-sidebar.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>

    <div id="wrapper">

        <!-- Sidebar -->
        <div id="sidebar-wrapper">
            <ul class="sidebar-nav">
                <li class="sidebar-brand">
                  <a href="#">
                    Odin Registration Page
                  </a>
                </li>
                <li>
                  <a href="index.php">Login</a>
                </li>
            </ul>
        </div>
        <!-- /#sidebar-wrapper -->

        <div id="page-content-wrapper">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-lg-12">
                      <a href="#menu-toggle" id="menu-toggle">
                        <img src="img/menu.svg" style="padding-left:30px;">
                      </a>

                      <!-- This set of php code displays the messages and then removes them if they are present -->
                      <h2 class="form-signin-heading" style="color:red;"> <!-- style="color:red;font-size:160%;width:100%;text-align:left;"> -->
                        <?php if(!empty($_SESSION['Message'])) { echo $_SESSION['Message']; } ?>
                      </h2>
                      <?php unset($_SESSION['Message']); ?>

                      <!-- Builds the form to accept register data and then runs register-run -->
                      <form class="form-signin" method="POST" action="register-run.php" role="form">
                        <h2 class="form-signin-heading">Odin Registration</h2>
                        <input type="text" class="form-control" name="user" placeholder="Username" required autofocus>
                        <input type="text" class="form-control" name="first" placeholder="First Name" required autofocus>
                        <input type="text" class="form-control" name="last" placeholder="Last Name" required autofocus>
                        <input type="email" class="form-control" name="email" placeholder="Email" required autofocus>
                        <input type="password" class="form-control" name="pass" placeholder="Password" required>
                        <button id="button" class="btn btn-lg btn-primary btn-block" type="submit" name="submit" href="login.php">Register</button>
                        <img src="img/logo_transparency.png" style="width:300px; height: 300px;padding-top: 20px;">
                      </form>
                    </div>
                </div>
            </div>
        </div>

    </div>
    <!-- /#wrapper -->

    <!-- jQuery Version 1.11.0 -->
    <script src="js/jquery-1.11.0.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>

    <!-- Menu Toggle Script -->
    <script>
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });
    $("#wrapper").toggleClass("toggled");
    </script>


</body>

</html>
