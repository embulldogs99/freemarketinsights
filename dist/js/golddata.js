


// jQuery
$.getScript('/js/papaparse.js', function()
{




  var client=new XMLHttpRequest();
  client.open("Get","/csv/spxvsgoldata.csv",true);
  client.send();
  client.onreadystatechange=function(){
    var obj=Papa.parse(client.responseText, {delimiter:",", header:true});

    var output='';
    for (var i=0;i<obj.length;i++){
      output+=obj[i];
    }

    document.getElementById('goldata').innerHTML=output;
  };



});
