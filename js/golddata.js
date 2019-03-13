


// jQuery
$.getScript('/js/papaparse.js', function()
{




  var client=new XMLHttpRequest();
  client.open("Get","/csv/spxvsgoldata.csv",true);
  client.send();
  client.onreadystatechange=function(){
    var obj=Papa.parse(client.responseText);

    var output='';
    for (var i=0;i<obj.data.length;i++){
      output+=obj.data[i];
    }

    document.getElementById('goldata').innerHTML=output;
  };



});
