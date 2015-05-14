<?php
ini_set('display_errors', 'On');
error_reporting(E_ALL);

  // Start session
  session_start();
  header('Content-Type: text/xml');
  // opens xml.file
  $myfile = fopen("xml.txt", "w") or die("Unable to open file!");

  $string = "";
  $fields = $_POST['OtherFields'];
  if(empty($fields))
  {
    // Error message if no fields were selected
    $_SESSION['Message'] = "You didn't select any fields!";
  }
  else
  {
    // Gets ticker and market from the selectfields.php
    $ticker = $_SESSION['Ticker'];
    $market = $_SESSION['Market'];
    // Begins building xml file
    $string = "<?xml version=\"1.0\"?><data><ticker symbol=\"$ticker\" market=\"$market\">";

    // adds each selected field to the xml file
    foreach($fields as $selectedOption)
    {
      $string .= "<field>$selectedOption</field>";
    }
    // Finishes the xml file
    $string .= "</ticker></data>";
    print($string);
    // writes the xml
    fwrite($myfile, $string);
    // sets message
    $_SESSION['Message'] = "Fetch XML created!";
  }
  // closes the file and navigates back to mainpage
  fclose($myfile);
  header('Location: mainpage.php');
?>
