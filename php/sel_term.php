<?php  

$link=mysqli_connect("localhost","root","admin", "smart" );  
if (!$link)  
{  
    echo "MySQL 접속 에러 : ";
    echo mysqli_connect_error();
    exit();  
}  

mysqli_set_charset($link,"utf8");

$date=$_POST["date"];

$sql="SELECT * FROM term WHERE date='$date'";

$result=mysqli_query($link,$sql);
$data = array();   
if($result){  
    
    while($row=mysqli_fetch_array($result)){
        array_push($data, 
            array('id'=>$row[0],
            'stime'=>$row[2],
            'etime'=>$row[3],
            'laver'=>$row[4],
            'raver'=>$row[5]

        ));
    }

	header('Content-Type: application/json; charset=utf8');
	$json = json_encode(array("data"=>$data), JSON_PRETTY_PRINT+JSON_UNESCAPED_UNICODE);
	echo $json;
}  
else{  
    echo "SQL문 처리중 에러 발생 : "; 
    echo mysqli_error($link);
} 


 
mysqli_close($link);  
   
?>
