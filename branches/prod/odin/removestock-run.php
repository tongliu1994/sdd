
<?php
ini_set('display_errors', 'On');
error_reporting(E_ALL);

	include("config.php");

	function RemoveStock()
	{
		// Starts session
		session_start();
		// connects to database
		$mysqli = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
		if($mysqli->connect_errno)
		{
			$_SESSION['Message'] = "MySQL error no {$mysqli->connect_errno} : {$mysqli->connect_error}";
			exit();
		}

		// checks if there are any checked stocks to delete and outputs an error if it is
		if(isset($_POST["stockToDelete"]))
		{
			$aStocks = $_POST['stockToDelete'];

			// checks if the list of checked stocks is empty and outputs a message
			if(empty($aStocks))
			{
				$_SESSION['Message'] = "You didn't select any stocks to delete!";
			}
			else
			{
				// Gets the count of checked checkboxes
				$n = count($aStocks);

				// Loops through all checked checkboxes
				for($i=0; $i < $n; $i++)
				{
					// Builds sql query to delete selected stocks and outputs associated messages
					$sql = "DELETE FROM StockData WHERE StockID = '{$aStocks[$i]}'";
					$result = $mysqli->query($sql);
					if($result)
					{
						$_SESSION['Message'] .= "Successfully deleted stock[$aStocks[$i]]! <br>";
						//header('Location: mainpage.php');
					}
					else
					{
						$_SESSION['Message'] .= "Failed to delete stock[$aStocks[$i]]! <br>";
						//header('Location: removeportfolio.php');
					}
				}
				// Navigate to mainpage
				header('Location: mainpage.php');
			}
		}
		else
		{
			// Navigate back to removestock
			$_SESSION['Message'] = "You didn't select any stocks to delete!";
			header('Location: removestock.php');
		}
	}


	if(isset($_POST['submit']))
	{
		RemoveStock();
	}
?>
