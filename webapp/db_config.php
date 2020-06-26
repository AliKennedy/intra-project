<?php  
define('USER', 'ali');
define('PASSWORD', 'Computing20*');
define('HOST', 'localhost');
define('DATABASE', 'intraproject');

try {
	$conn = new PDO("mysql:host=".HOST.";dbname=".DATABASE, USER, PASSWORD);
} catch (PDOException $err) {
	exit("Error: ".$err->getMessage());
}
?>