<html>
<head>
	<meta charset="UTF-8">
	<meta name="description" content="Log out page. Option to sign up or back in">
	<meta name="author" content="Alison Kennedy">
	
	<title>ALRS HomePage</title>
	<link rel="stylesheet" href="styles.css">
</head>
<body>
	<header>
		<h1>ALRS Sanitisation</h1>
	</header>

	<div class="nav-bar">
		<ul id="nav-list">
			<li id="nav-item"><a href="index.php">Intro</a></li>
			<li id="nav-item"><a href="signup.php">Sign Up</a></li>
			<li id="nav-item"><a href="login.php">Log In</a></li>
		</ul>
	</div>

<?php
	session_start();

	$_SESSION = array(); //reset session variables

	//delete session cookie
	if (ini_get("session.use_cookies")) {
		$parameters = session_get_cookie_params();
		setcookie(session_name(), '', time() - 42000, $parameters["path"],
			$parameters["domain"], $parameters["secure"], $parameters["httponly"]);
	}

	//destroy session
	session_destroy();
?>

<p>You are now logged out.</p>

</body>
<div class="footer">
<footer>
	<p>Author: Alison Kennedy, Computer Applications and Software Engineering, DCU<br>
		<a href="mailto:alison.kennedy55@mail.dcu.ie">alison.kennedy55@mail.dcu.ie</a>
	</p>
</footer>
</div>
</html>