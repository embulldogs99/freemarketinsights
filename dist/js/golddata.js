

var client=new XMLHttpRequest();
client.open("Get","/csv/spxvsgoldata.csv",true);
client.send();
client.onreadystatechange=function(){
  var obj=$.csv.toObjects(client.responseText);
  document.getElementById('goldata').innerHTML=obj;
};
