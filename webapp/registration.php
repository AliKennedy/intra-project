<html>
<head>
	<meta charset="UTF-8">
	<meta name="description" content="Log in page">
	<meta name="author" content="Alison Kennedy">
	
	<title>ALRS Sign Up</title>
	<link rel="stylesheet" href="styles.css">
</head>
<body>
	<header>
		<h1>ALRS Sanitisation</h1>
	</header>
	<div class="nav-bar">
		<ul id="nav-list">
			<li id="nav-item"><a href="user_home.php">User Home</a></li>
		</ul>
	</div>

<?php

include('db_config.php');
session_start();


//check if the user has pressed the sign up button
if (isset($_POST['signup'])) {

	$username = $_POST['username'];
	$email = $_POST['email'];
	$password = $_POST['password'];
	$hashed_password = password_hash($password, PASSWORD_DEFAULT); //store hashed password in database

	$query = $conn->prepare("SELECT * FROM users WHERE email=:email");
	$query->bindParam("email", $email, PDO::PARAM_STR);
	$query->execute();

	if ($query->rowCount() > 0) {
		echo '<p class="error">The email address you entered is already registered to a user on this site.</p>';
	}

	elseif ($query->rowCount() == 0) {
		$query = $conn->prepare("INSERT INTO users(username,password,email) VALUES (:username,:hashed_password,:email)");
		$query->bindParam("username", $username, PDO::PARAM_STR);
		$query->bindParam("hashed_password", $hashed_password, PDO::PARAM_STR);
		$query->bindParam("email", $email, PDO::PARAM_STR);
		$result = $query->execute();

		if ($result) {
			echo '<p class="success">You have successfully signed up!</p>';
			header('Refresh: 8; user_home.php');
			echo '<p> You will be directed to your homepage in 5 seconds. If not... <a href="user_home.php">click here</a></p>';
		} else {
			echo '<p class="error">There was an issue with signing you up. Please try again.</p>';
		}
	}

}

?>

</body>

<footer>
	<p>Author: Alison Kennedy, Computer Applications and Software Engineering, DCU<br> 
		<a href="mailto:alison.kennedy55@mail.dcu.ie">alison.kennedy55@mail.dcu.ie</a>
	</p>
</footer>
</html>