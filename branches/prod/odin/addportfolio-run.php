
<?php
ini_set('display_errors', 'On');
error_reporting(E_ALL);

	include("config.php");

	function AddPortfolio()
	{
		// Starts Session
		session_start();
		// Connects to database
		$mysqli = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
		if($mysqli->connect_errno)
		{
			// Checks if the connection worked, display an error if it didn't
			$_SESSION['Message'] = "MySQL error no {$mysqli->connect_errno} : {$mysqli->connect_error}";
			exit();
		}

		// Gets portfolio name and description from html form
		$pname = $_POST['pname'];
		$description = $_POST['description'];

		//print($_SESSION['UserID']);

		// Create the sql query
		$sql = "INSERT INTO PortfolioData (PortfolioName, OwnerID, Description) VALUES ('{$pname}', '{$_SESSION['UserID']}', '{$description}')";

		// Run the sql query and store the response
		$result = $mysqli->query($sql);
		if($result)
		{
			// If the result is not null then the query was successful, display success message and navigate back to the mainpage
			$_SESSION['Message'] = "Successfully added portfolio!";
			header('Location: mainpage.php');
		}
		else
		{
			// If the result is null then the query failed, display an error message and navigate back to the addportfolio page
			$_SESSION['Message'] = "Failed to add portfolio!";
			header('Location: addportfolio.php');
		}
	}


	if(isset($_POST['submit']))
	{
		AddPortfolio();
	}
?>
