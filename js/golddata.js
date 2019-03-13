


// jQuery
$.getScript('/js/papaparse.js', function()
{




  var client=new XMLHttpRequest();
  client.open("Get","/csv/spxvsgoldata.csv",true);
  client.send();
  client.onreadystatechange=function(){
    var obj=Papa.parse(client.responseText);
    document.getElementById('goldata').innerHTML=obj;
  };



});
