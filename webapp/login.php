<html>
<head>
	<meta charset="UTF-8">
	<meta name="description" content="Log in page">
	<meta name="author" content="Alison Kennedy">
	
	<title>ALRS Login</title>
	<link rel="stylesheet" href="styles.css">
</head>
<body>
	<header>
		<h1>ALRS Sanitisation</h1>
	</header>
		<div class="nav-bar">
		<ul id="nav-list">
			<li id="nav-item"><a href="signup.php">Sign Up</a></li>
		</ul>
	</div>
	<!-- form to collect user's username and password -->
	<form method="post" action="login_action.php" name="signin-form" align="center">
		<div class="form-element">
			<label>Username</label>
			<input type="text" name="username" required />
		</div>
		<div class="form-element">
			<label>Password</label>
			<input type="password" name="password" required />
		</div>
		<div class="login_button">
			<button type="submit" name="login" value="login">Log In</button>
		</div>
	</form>
</body>

<footer>
	<p>Author: Alison Kennedy, Computer Applications and Software Engineering, DCU<br> 
		<a href="mailto:alison.kennedy55@mail.dcu.ie">alison.kennedy55@mail.dcu.ie</a>
	</p>
</footer>
</html>