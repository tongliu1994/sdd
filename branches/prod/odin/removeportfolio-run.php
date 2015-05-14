
<?php
ini_set('display_errors', 'On');
error_reporting(E_ALL);

	include("config.php");

	function RemovePortfolio()
	{
		// Starts session
		session_start();

		// connects to database and outputs an error if the connect fails
		$mysqli = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
		if($mysqli->connect_errno)
		{
			$_SESSION['Message'] = "MySQL error no {$mysqli->connect_errno} : {$mysqli->connect_error}";
			exit();
		}

		// Checks if there are any checked porfolios, outputs an error if there arent
		if(isset($_POST["portToDelete"]))
		{
			$aPorts = $_POST['portToDelete'];

			// Checks if the checked portfolios were empty, if they are output a message
			if(empty($aPorts))
			{
				$_SESSION['Message'] = "You didn't select any portfolios to delete!";
			}
			else
			{
				// Get count of all checked portfolios
				$n = count($aPorts);

				// Loop through all checked portfolios
				for($i=0; $i < $n; $i++)
				{
					// Build and run sql to delete the portfolio from the portfolio table with associated messages
					$sql = "DELETE FROM PortfolioData WHERE PortfolioID = '{$aPorts[$i]}'";
					$result = $mysqli->query($sql);
					if($result)
					{
						$_SESSION['Message'] .= "Successfully deleted portfolio[$aPorts[$i]]! <br>";
						//header('Location: mainpage.php');
					}
					else
					{
						$_SESSION['Message'] .= "Failed to delete portfolio[$aPorts[$i]]! <br>";
						//header('Location: removeportfolio.php');
					}
				}
				// return to the mainpage
				header('Location: mainpage.php');
			}
		}
		else
		{
			// If there aren't any checkboxes checked return to remove portfolio
			$_SESSION['Message'] = "You didn't select any portfolios to delete!";
			header('Location: removeportfolio.php');
		}
	}


	if(isset($_POST['submit']))
	{
		RemovePortfolio();
	}
?>
