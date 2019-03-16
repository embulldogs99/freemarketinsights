

function portfoliorun(){

  var xhttp=new XMLHttpRequest();
  xhttp.onreadystatechange=function(){
    if (this.readyState ==4 && this.status ==200){
      var response=JSON.parse(xhttp.responseText);
      var output='';
      for (var i=0;i<response.length;i++){

        if(response[i].to_char==null){tg='-'}else{tg=response[i].to_char}

        output +=
          '<tr>'+
          '<td><a href="http://www.google.com/search?q='+response[i].ticker+'+stock+price"  target="_blank" >'+response[i].ticker+'</a></td>'+
          '<td>Current Price: $<b>'+response[i].price+'</b><br>'+
          'Initial Target Price: $<b>'+response[i].target_price+'</b><br>'+
          'Last Target Mention: $<b>'+response[i].target+'</b><br>'+
          'Mention Date:<b> '+tg+'</b></td>'+

          '<td><b>'+((response[i].target-response[i].price)/response[i].price*100).toFixed(2)+'%'+'</b></td>'+
          '<td><a href="/html/trend?'+response[i].ticker+'"  target="_blank" ><img src="/portpics/'+response[i].ticker+'+tt.png" width="400" height="300"/></a></td>'+
          '<td><a href="/html/trend?'+response[i].ticker+'" target="_blank"><img src="/portpics/'+response[i].ticker+'+divs.png" width="400" height="300"/></a></td>'+
          '</tr>';

      }

      document.getElementById('port').innerHTML=output;
      }
    };
    xhttp.open("Get", "/json/portfolio.json",true);
    xhttp.send();

}

portfoliorun();
