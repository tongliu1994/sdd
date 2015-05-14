
<?php
ini_set('display_errors', 'On');
error_reporting(E_ALL);

	include("config.php");

	function AddStock()
	{
		// Start session
		session_start();

		// Connect to the database
		$mysqli = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
		if($mysqli->connect_errno)
		{
			// Checks if the connection worked, display an error if it didn't
			$_SESSION['Message'] = "MySQL error no {$mysqli->connect_errno} : {$mysqli->connect_error}";
			exit();
		}

		// Checks if the checkboxes had any data
		if(isset($_POST["portToAdd"]))
		{
			$aPorts = $_POST['portToAdd'];

			// Checks if the checkbox of ports is empty and returns a meesage if they are
			if(empty($aPorts))
			{
				$_SESSION['Message'] = "You didn't select any portfolios to add to!";
			}
			else
			{
				// Gets the count of the number of checked boxes
				$n = count($aPorts);

				// Loops through all the checked boxes
				for($i=0; $i < $n; $i++)
				{
					// Stores if the element exists
					$exists = 0;

					// Builds sql query to see if stocks exist in the portfolio with the assocaited ticker symbol
					$sql1 = "SELECT * from StockData WHERE PortfolioID = '{$aPorts[$i]}' AND s0 = '{$_POST['InputName']}'";
					$result = $mysqli->query($sql1);
					if($result->num_rows != 0)
					{
						// If the data already exists then set exists to 1
						$exists = 1;
					}

					// If the data exists then we display a message that the stock already exists in the portfolio
					if($exists == 1)
					{
						$_SESSION['Message'] .= "Stock already exists within portfolio[$aPorts[$i]]! <br>";
					}
					else
					{
						//	If the data doesn't exist then we build an sql query to insert the stocks to the assocaited portfolio
						$sql2 = "INSERT INTO StockData (PortfolioID, s0) VALUES ('{$aPorts[$i]}', '{$_POST['InputName']}')";
						if($mysqli->query($sql2))
						{
							// If the query is successful display a message
							$_SESSION['Message'] .= "Successfully added stock to portfolio[$aPorts[$i]]! <br>";
						}
					}
				}

				// Store in session the market and ticker symbol
				$_SESSION['Ticker'] = $_POST['InputName'];
				$_SESSION['Market'] = $_POST['MarketName'];

				// navigate to the selectfields page
				header('Location: selectfields.php');
				//header('Location: mainpage.php');
			}
		}
		else
		{
			// No portfolios were selected, navigate back to the addstock page
			$_SESSION['Message'] = "You didn't select any portfolios to add to!";
			header('Location: addstock.php');
		}
	}


	if(isset($_POST['submit']))
	{
		AddStock();
	}
?>
