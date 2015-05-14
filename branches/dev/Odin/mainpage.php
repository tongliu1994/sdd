
<!DOCTYPE html>
<?php session_start();
  //$fieldsInfo = array('StockID','PortfolioID','time','c8','g3','a0','b2','a5','a2','b0','b3','b6','b4','c1','c0','m7','m5','k4','j5','p2','k2','c6','c3','c4','h0','g0','m0','m2','w1','w4','r1','d0','y0','e0','j4','e7','e9','e8','q0','m3','f6','l2','g4','g1','g5','g6','v1','v7','d1','l1','k1','k3','t1','l0','l3','j1','j3','i0','n0','n4','t8','o0','i5','r5','r0','r2','m8','m6','k5','j6','p0','p6','r6','r7','p1','p5','s6','s1','j2','s7','x0','s0','t7','d2','t6','f0','m4','v0','k0','j0','w0');
  // Commented out for now due to Atom error that made everything else bright green :/
?>
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
                        Odin Main Page
                    </a>
                </li>
                <li>
                    To be added... Use cases (probably)
                </li>
                <li>
                  <a href="index.php">Back to Login</a>
                </li>
            </ul>
        </div>


        <div id="page-content-wrapper">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-lg-12">
                      <a href="#menu-toggle" id="menu-toggle">
                        <img src="img/menu.svg" style="padding-left:30px;">
                      </a>
                    <div class="dropdown" style="padding-right:50px;display:block;float:right;">
                      <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown">
                        <img src="img/gear.png">
                        <span class="caret"></span>
                      </button>
                      <ul class="dropdown-menu dropdown-menu-right" role="menu" aria-labelledby="dropdownMenu1">
                        <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Please Login</a></li>
                      </ul>
                    </div>

                      <form class="main">
                        <h4 stlye="color:red;">
                          <?php if(!empty($_SESSION['Message'])) { echo $_SESSION['Message']; } ?>
                        </h4>
                        <?php unset($_SESSION['Message']); ?>

                        <h1 style="text-align: center;">Odin Portfolio Manager</h1>
                        <h1 style="font-size:20px">
                          Welcome
                          <?php if(!empty($_SESSION['FirstName'])) { echo $_SESSION['FirstName']; } ?>
                          <?php if(!empty($_SESSION['LastName'])) { echo $_SESSION['LastName']; } ?>!
                        </h1>

                        <?php
                          include("config.php");
                          $mysqli = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
                          if($mysqli->connect_errno)
                          {
                            $_SESSION['Message'] = "MySQL error no {$mysqli->connect_errno} : {$mysqli->connect_error}";
                            header('Location: mainpage.php');
                          }
                          else
                          {
                              //$_SESSION['Message'] = "MySQL connection established!";
                              //header('Location: mainpage.php');
                              if(!empty($_SESSION['UserID']))
                              {
                                $userid = $_SESSION['UserID'];

                                $portfolioSql = "SELECT * from PortfolioData WHERE OwnerID = '$userid'";
                                $portfolioResult = $mysqli->query($portfolioSql);
                                if($portfolioResult->num_rows != 0)
                                {
                                  while($portfolioRow = mysqli_fetch_row($portfolioResult))
                                  {
                                    $stockString = "";

                                    $stockSql = "SELECT * from StockData WHERE PortfolioID = '$portfolioRow[0]'";
                                    $stockResult = $mysqli->query($stockSql);
                                    if($stockResult->num_rows != 0)
                                    {
                                      while($stockRow = mysqli_fetch_row($stockResult))
                                      {
                                        $fields = "";
                                        for ($i = 0; $i < count($stockRow); ++$i)
                                        {
                                          // FETCH ASSOCIATIVE? MAY FIX THESE PROBLEMS/HELP

                                          if($i == 0 || $i == 1 || $i == 2) // OR $i != 1 OR $i != 2)
                                          {}
                                          else
                                          {
                                            if($stockRow[$i] != NULL)
                                            {
                                              //$fields .= "<p>" . $fieldsInfo[$i] . ": " . $stockRow[$i] . "</p>";
                                              // Commented out for now due to an Atom error that made all other text bright green.
                                              // Made work difficult.
                                              $fields .= "<p>" . $stockRow[$i] . "</p>";
                                            }
                                          }
                                        }

                                        $stockTemp = "<div class=\"panel-group\" id=\"accordion\"><div class=\"panel panel-default\"><div class=\"panel-heading\"><h4 class=\"panel-title\"><a data-toggle=\"collapse\" data-parent=\"#accordionP$portfolioRow[0]S$stockRow[0]\" href=\"#collapseP$portfolioRow[0]S$stockRow[0]\">$stockRow[81]</a></h4></div><div id=\"collapseP$portfolioRow[0]S$stockRow[0]\" class=\"panel-collapse collapse in\"><div class=\"panel-body\">$fields</div></div></div></div>";
                                        //print($stockTemp);
                                        $stockString .= $stockTemp;
                                      }
                                    }
                                    else
                                    {
                                      $stockString .= "No stocks to show! Try adding a stock in the sidebar!";
                                    }

                                    $string = "<div class=\"panel-group\" id=\"accordion\"><div class=\"panel panel-default\"><div class=\"panel-heading\"><h4 class=\"panel-title\"><a data-toggle=\"collapse\" data-parent=\"#accordionP$portfolioRow[0]\" href=\"#collapseP$portfolioRow[0]\"> $portfolioRow[1] </a></h4></div><div id=\"collapseP$portfolioRow[0]\" class=\"panel-collapse collapse in\"><div class=\"panel-body\">$stockString</div></div></div></div>";
                                    print($string);
                                  }
                                }
                                else
                                {
                                  print("No portfolios to show! Try adding a portfolio in the sidebar!");
                                }
                              }
                              else
                              {
                                $_SESSION['Message'] = "Log in to view data!";
                                header('Location: mainpage.php');
                              }
                          }
                        ?>

                        <h2><img src="img/logo_transparency.png" style="width:300px; height: 300px;padding-top: 20px;"></h2>
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
