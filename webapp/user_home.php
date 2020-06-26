<html>
<head>
	<meta charset="UTF-8">
	<meta name="description" content="User homepage to access dispenser data.">
	<meta name="author" content="Alison Kennedy">
	<!-- autorefresh every 30 seconds-->
	<!--<meta http-equiv="refresh" content="30">-->
	
	<title>ALRS HomePage</title>
	<link rel="stylesheet" href="styles.css">
</head>
<body>
	<header>
		<h1>ALRS Sanitisation</h1>
	</header>
	<div class="nav-bar">
		<ul id="nav-list">
			<li id="nav-item"><a href="logout.php">Log Out</a></li>
		</ul>
	</div>

	<form method="post" action="register_dispenser.php" name="add_new_dispenser_form">
	<div class="form-element">
		<label>Dispenser ID</label>
		<input type="text" name="dispenserid" required />
	</div>
	<button type="submit" name="register_dispenser" value="register_dispenser">Register New Dispenser</button>
	</form>

<?php  
	session_start();

	include('db_config.php'); //database configuration
	$userid = $_SESSION[user_id];

	//display notifications
	$query = $conn->prepare("SELECT * FROM notifications WHERE dispenser_id IN (SELECT id FROM dispensers WHERE user_id = :userid)");
	$query->bindParam("userid", $userid, PDO::PARAM_STR);
	$query->execute();

	$result = $query->fetchAll(PDO::FETCH_ASSOC);
	if ($result) {
		echo "<div class='notifications'><h3>Notifications</h3>";
		echo "<ul id='notification-list'>";
		foreach($result as $row) {
			echo "<li id='notification-item'><h4>".$row["dispenser_id"]."</h4> ".$row["message"]." ".$row["date_time"]."</li>";
		}
		echo "</ul></div>";
	} else {
		echo "<h3>No notifications at the moment!</h3>";

	}

	//display latest record for each dispenser
	$query1 = $conn->prepare("SELECT * FROM dispenserdata d1 WHERE date_time = (SELECT MAX(date_time) FROM dispenserdata d2 WHERE d1.id = d2.id) AND d1.id IN (SELECT id FROM dispensers WHERE user_id = :userid) ORDER BY id, date_time");
	$query1->bindParam("userid", $userid, PDO::PARAM_STR);
	$query1->execute();

	$result1 = $query1->fetchAll(PDO::FETCH_ASSOC);
	if ($result1) {
		echo "<table><caption>Latest Dispenser Updates</caption><tr><th>Dispenser ID</th><th>Fluid %</th><th>Uses Since Last Update</th><th>ALerts Issued</th><th>Ignored</th><th>Timestamp</th></tr>";
		foreach($result1 as $row1) {
			echo "<tr><td>".$row1['id']."</td><td>".$row1['fluidlevel']."</td><td>".$row1['uses']."</td><td>".$row1['alerts']."</td><td>".$row1['ignored']."</td><td>".$row1['date_time']."</td></tr>";
		}
		echo "</table>";
	}

	$query2 = $conn->prepare("SELECT * FROM dispenserdata WHERE id IN (SELECT id FROM dispensers WHERE user_id=:userid)");
	$query2->bindParam("userid", $userid, PDO::PARAM_STR);
	$query2->execute();

	//All dispenser data from today's date
	$result2 = $query2->fetchAll(PDO::FETCH_ASSOC);
	if ($result2) {
		echo "<table><caption>All of Today's Dispenser Data</caption><tr><th>Dispenser ID</th><th>Fluid %</th><th>Uses Since Last Update</th><th>Alerts Issued</th><th>Ignored</th><th>Timestamp</th></tr>";
		foreach ($result2 as $row2) {
			echo "<tr><td>".$row2['id']."</td><td>".$row2['fluidlevel']."</td><td>".$row2['uses']."</td><td>".$row2['alerts']."</td><td>".$row2['ignored']."</td><td>".$row2['date_time']."</td></tr>";
		}
		echo "</table>";
	}
?> <!-- Text field to enter dispenser ID and link it with your account. Adds your user_id to dispenser id's row in dispenser table-->


</body>

<div class="footer">
<footer>
	<p>Author: Alison Kennedy, Computer Applications and Software Engineering, DCU<br> 
		<a href="mailto:alison.kennedy55@mail.dcu.ie">alison.kennedy55@mail.dcu.ie</a>
	</p>
</footer>
</div>
</html>