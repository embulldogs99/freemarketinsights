

function mbear(){
var xhttp2=new XMLHttpRequest();
xhttp2.onreadystatechange=function(){
  if (this.readyState ==4 && this.status ==200){
    var response2=JSON.parse(xhttp2.responseText);
    var output2='';
    for (var i=0;i<5;i++){
      if (response2[i].divyield==null){divyield="-";}else{divyield=response[i].divyield;}
      output2 += "<div class='horizontal'>"+
      "<div class='newscount'>"+i+"</div>"+
      '<tr><td class="hometablenote"><a href="http://www.google.com/search?q='+response2[i].note+'"  target="_blank" >'+response2[i].note+'</a></td></tr>'+
      '<tr><td>Last Price</td>'+'<td>$'+response2[i].price+'</td>'+
      '<td>Expected Return</td>'+'<td>'+response2[i].returns+'%'+'</td>'+
      '<td>Dividend Yield</td>'+'<td>'+divyield+'</td>'+
      '<td><a href="http://www.google.com/search?q='+response2[i].ticker+'+stock+price"  target="_blank" >'+response2[i].ticker+'</a></td>'+
        '</tr></div>';
    }

    document.getElementById('mbear').innerHTML=output2;
    }
  };
  xhttp2.open("Get", "/json/marketbears.json",true);
  xhttp2.send();
}

mbear();
