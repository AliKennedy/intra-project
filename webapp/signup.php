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
			<li id="nav-item"><a href="login.php">Log In</a></li>
		</ul>
	</div>

	<!-- form to collect user's sign up information -->
	<form method="post" action="registration.php" name="signup-form" align="center">
		<div class="form-element">
			<label>Username</label>
			<input type="text" name="username" required />
		</div>
		<div class="form-element">
			<label>Email</label>
			<input type="email" name="email" required />
		</div>
		<div class="form-element">
			<label>Password</label>
			<input type="password" name="password" required />
		</div>
		<button type="submit" name="signup" value="signup">Sign Up</button>
	</form>
</body>

<footer>
	<p>Author: Alison Kennedy, Computer Applications and Software Engineering, DCU<br> 
		<a href="mailto:alison.kennedy55@mail.dcu.ie">alison.kennedy55@mail.dcu.ie</a>
	</p>
</footer>
</html>