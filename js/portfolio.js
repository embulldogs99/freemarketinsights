

function portfoliorun(){

  var xhttp=new XMLHttpRequest();
  xhttp.onreadystatechange=function(){
    if (this.readyState ==4 && this.status ==200){
      var response=JSON.parse(xhttp.responseText);
      var output='<thead><tr><th>Ticker</th><th>Prices</th><th>Exp Return</th><th>Target Trend</th><th>Dividends Trend</th></tr></thead><tbody>';
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

      output+='</tbody>'
      document.getElementById('port').innerHTML=output;
      }
    };
    xhttp.open("Get", "/json/portfolio.json",true);
    xhttp.send();

}

function score(){
var client=new XMLHttpRequest();
client.open("Get","/json/portfoliofundamentalanalysis.json",true);
client.send();
client.onreadystatechange=function(){
  var response=JSON.parse(client.responseText);
  var output='';
  output+='<tr>'+
  '<th>Ticker</th>'+
  '<th>Last Price</th>'+
  '<th>Target Price</th>'+
  '<th>Stock Score</th>'+
  '<th>DebttoEquity</th>'+
  '<th>DivYield</th>'+
  '<th>ROA</th>'+
  '<th>ROE</th>'+
  '<th>AvgEPSgrowth</th>'+
  '</tr>';
  for (var i=0;i<response.length;i++){
    output+='<tr>'+
    '<td>'+response[i].ticker+'</td>'+
    '<td>$'+response[i].price+'</td>'+
    '<td>$'+response[i].target+'</td>'+
    '<td>'+(response[i].score).toFixed(2)+'</td>'+
    '<td>'+(response[i].debttoequity*100).toFixed(2)+'%</td>'+
    '<td>'+(response[i].divyield*100).toFixed(2)+'%</td>'+
    '<td>'+(response[i].roa*100).toFixed(2)+'%</td>'+
    '<td>'+(response[i].roe*100).toFixed(2)+'%</td>'+
    '<td>'+(response[i].avgepsgrowthscore).toFixed(2)+'</td>'+
    '</tr>';
  }
document.getElementById('stockscore').innerHTML=output;
};
}
score();

portfoliorun();
