
function run(){
var client=new XMLHttpRequest();
client.open("Get","/json/stockrank.json",true);
client.send();
client.onreadystatechange=function(){
  var response=JSON.parse(client.responseText);
  var output='';
  output+='<tr>'+
  '<th>Ticker</th>'+
  '<th>Last Price</th>'+
  '<th>Target Price</th>'+
  '<th>Stock Score</th>'+
  '<th>E/P</th>'+
  '<th>DivYield</th>'+
  '<th>Annual EPS</th>'+
  '<th>Five Year Low %</th>'+
  '<th>Bank</th>'+
  '</tr>';
  for (var i=0;i<response.length;i++){
    output+='<tr>'+
    '<td>'+response[i].ticker+'</td>'+
    '<td>$'+response[i].price+'</td>'+
    '<td>$'+response[i].target+'</td>'+
    '<td>'+(response[i].score).toFixed(2)+'</td>'+
    '<td>$'+(response[i].a_e_p).toFixed(2)+'</td>'+
    '<td>'+(response[i].divyield).toFixed(2)+'%</td>'+
    '<td>$'+response[i].a_eps+'</td>'+
    '<td>'+(response[i].fiveyrlow_percent*100).toFixed(2)+'%</td>'+
    '<td>'+response[i].bank+'</td>'+
    '</tr>';
  }
document.getElementById('stocksort').innerHTML=output;
};
}
run();
