<html>
<head>
	<title>ALRS Login</title>
</head>
<body>
<?php

//access to intraproject database
include('db_config.php');
session_start();

//check if user has pressed login button
if (isset($_POST['login'])) {

	$username = $_POST['username']; //username
	$password = $_POST['password']; //password

	//check if username is in databse
	$query = $conn->prepare("SELECT * FROM users WHERE username=:username");
	$query->bindParam("username", $username, PDO::PARAM_STR);
	$query->execute();

	$result = $query->fetch(PDO::FETCH_ASSOC);


	if (!$result) { //no result, username is incorrect
		echo '<p class="error">Username or password is incorrect.</p>';
	} else { //username exists in database
		if (password_verify($password, $result['password'])) {
			$_SESSION[user_id] = $result['id']; //start a user session
			echo '<p class="success">You are now logged in!</p>';
			header("Location: user_home.php"); //redirect to homepage
			exit;
		} else { //password is incorrect
			echo '<p class="error">Username or password is incorrect.</p>';
		}
	}
}

?>
</body>
</html>