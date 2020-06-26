<?php

include('db_config.php');
session_start();


//check if the user has pressed the sign up button
if (isset($_POST['register_dispenser'])) {

	$dispenser_id = $_POST['dispenserid'];
	$user = $_SESSION[user_id];

	//echo "" . $_SESSION[user_id];

	$query = $conn->prepare("UPDATE dispensers SET user_id=:user WHERE id=:dispenser_id");
	$query->bindParam("user", $user, PDO::PARAM_STR);
	$query->bindParam("dispenser_id", $dispenser_id, PDO::PARAM_STR);
	$result = $query->execute();

	if ($result) {
		echo '<p class="success">dispenser succesfully linked to your account!</p>';
		header('Refresh: 5; user_home.php');
		echo '<p> You will be redirected back to your homepage in 5 seconds. If not... <a href="user_home.php">click here</a></p>';
	} else {
		echo '<p class="error">There was an issue linking this dispenser to your account.</p>';
	}
}




//prone to sql injection
?>