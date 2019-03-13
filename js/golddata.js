
var csv = require('/js/jquery-csv.js');

var client=new XMLHttpRequest();
client.open("Get","/csv/spxvsgoldata.csv",true);
client.send();
client.onreadystatechange=function(){
  var response=JSON.parse(client.responseText);

var obj=$.csv.toObjects(response);
console.log(obj);
}
