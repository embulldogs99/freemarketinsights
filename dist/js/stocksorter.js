
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
  '<th>Annual EPS</th>'+
  '<th>Five Year Low Distance</th>'+
  '</tr>';
  for (var i=0;i<response.length;i++){
    if (response.fiveyrlow_distance!='-'){fyld='-';}
      else{fyld=(response.fiveyrlow_distance*100).toFixed(2)+'%';}
    output+='<tr>'+
    '<td>'+response.ticker+'</td>'+
    '<td>$'+response.price+'</td>'+
    '<td>$'+response.target+'</td>'+
    '<td>'+response.score+'</td>'+
    '<td>$'+response.a_eps+'</td>'+
    '<td>'+fyld+'</td>'+
    '</tr>';
  }
document.getElementById('stocksort').innerHTML=output;
};
}
run();
