<html>
<body>

<?php 
function publishDst($dst) {
    shell_exec('mosquitto_pub -t robot/dst -m "$dst"');
    return $dst;
}

if (isset($_POST['dst']) {
    $current_dst = publishDst($_POST['dst']);
} 
?>

<form action="./v1/robot_go">
	<input type="submit" value="Enable Movement">
</form>
<form action="./v1/robot_stop">
	<input type="submit" value="Disable Movement">
</form>

<?php 
    if (isset($current_dst)) { 
        echo "Current destination: $current_dst";
    }
    else {
        echo "Current destination: none";
    }
?>

<p>Select a destination:<p>
<form name="chooseDst" action="" method="post">
    1 <input type="radio" name="dst" value="1" checked><br>
    2 <input type="radio" name="dst" value="2"><br>
    3 <input type="radio" name="dst" value="3"><br>
    <input name="Submit" type="submit">
</form>


</body>
</html>
