<!DOCTYPE html>
<html lang="en">
<head>
<title>Parkman</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="styles.css">
</head>
<body>

<div class="header">
  <h1>PARKMAN</h1>
  <h4>Management report</h4>
</div>
 

<?php
$servername = "localhost";
$username = "faris";
$password = "password";
$dbname = "parkman";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
} 

// $sql = "SELECT  from parked";
$price = mysqli_fetch_assoc($conn->query("SELECT const from constants where id='price'"))["const"];
$space = mysqli_fetch_assoc($conn->query("SELECT const from constants where id='spaces'"))["const"];
?>

<div class="row">
  <div class="column" style="background-color:#eee;">

    <div class="current-status">
    <div class="price">
      <p>Price per hour:</p>
      <p style="padding-left: 180px;">$<?php echo $price; ?></p>
    </div>
      <div>
      <p>Current occupancy:</p>
      <div class="occupancy">
        <!-- TODO: php & sql -->
        <?php
        $occupied = mysqli_fetch_assoc($conn->query("SELECT count(id) as count FROM parked WHERE exit_time IS NULL"))["count"];
        $percentage = $occupied/$space*100;
        
        if ($percentage >= 100):
          $color = "red";
        elseif ($percentage > 66):
          $color = "orange";
        elseif ($percentage > 33):
          $color = "yellow";
        else:
          $color = "limegreen";
        endif;
        $html = "<div style='background-color: ".$color.";'>".$occupied."/".$space."</div><div>";
        $html .= $percentage;
        $html .="%</div>";
        echo $html;
      ?>
      </div>
      </div>
    
      <?php
        $day = mysqli_fetch_array($conn->query("SELECT count(id) as 'count', avg(TIME_TO_SEC(TIMEDIFF(exit_time, entrance_time))/3600) as 'time' FROM parked WHERE day(exit_time)=day(sysdate())"));
        array_push($day, $day[1]*$price);
        if ($day[0] == 0) {
          $day[1]=0;$day[2]=0;
        }          
        $month = mysqli_fetch_array($conn->query("SELECT count(id) as 'count', avg(TIME_TO_SEC(TIMEDIFF(exit_time, entrance_time))/3600) as 'time' FROM parked WHERE month(exit_time)=month(sysdate())"));
        array_push($month, $month[1]*$price);
        if ($month[0] == 0) {
          $month[1]=0;$month[2]=0;
        }        
        $year = mysqli_fetch_array($conn->query("SELECT count(id) as 'count', avg(TIME_TO_SEC(TIMEDIFF(exit_time, entrance_time))/3600) as 'time' FROM parked WHERE year(exit_time)=year(sysdate())"));
        array_push($year, $year[1]*$price);
        if ($year[0] == 0) {
          $year[1]=0;$year[2]=0;
        }        
        $ever = mysqli_fetch_array($conn->query("SELECT count(id) as 'count', avg(TIME_TO_SEC(TIMEDIFF(exit_time, entrance_time))/3600) as 'time' FROM parked"));
        array_push($ever, $ever[1]*$price);
        if ($ever[0] == 0) {
          $ever[1]=0;$ever[2]=0;
        }        
        ?>
      
    </div>

  <div class="tabela">
      <table class="tg">
      <thead>
        <tr>
          <th></th>
          <th>Today</th>
          <th>This month</th>
          <th>This year</th>
          <th>Total</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Total cars<br></td>
          <td><?php echo $day[0]; ?></td>
          <td><?php echo $month[0]; ?></td>
          <td><?php echo $year[0]; ?></td>
          <td><?php echo $ever[0]; ?></td>
        </tr>
        <tr>
          <td>Average time parked</td>
          <td><?php echo number_format($day[1], 2); ?> h</td>
          <td><?php echo number_format($month[1], 2); ?> h</td>
          <td><?php echo number_format($year[1], 2); ?> h</td>
          <td><?php echo number_format($ever[1], 2); ?> h</td>
        </tr>
        <tr>
          <td>Average paid price</td>
          <td>$<?php echo number_format($day[2], 2); ?></td>
          <td>$<?php echo number_format($month[2], 2); ?></td>
          <td>$<?php echo number_format($year[2], 2); ?></td>
          <td>$<?php echo number_format($ever[2], 2); ?></td>
        </tr>
      </tbody>
      </table>
  </div> 
  </div>
</div>

</body>
</html>
