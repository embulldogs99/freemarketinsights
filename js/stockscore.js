
function run(){
var client=new XMLHttpRequest();
client.open("Get","/json/recentfundamentalanalysis.json",true);
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
document.getElementById('stocksort').innerHTML=output;
};
}
run();
