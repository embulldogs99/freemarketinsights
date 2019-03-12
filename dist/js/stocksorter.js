
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
    if (response[i].fiveyrlow_distance!='-'){fyld='-';}
      else{fyld=(response[i].fiveyrlow_distance*100).toFixed(2)+'%';}
    output+='<tr>'+
    '<td>'+response[i].ticker+'</td>'+
    '<td>$'+response[i].price+'</td>'+
    '<td>$'+response[i].target+'</td>'+
    '<td>'+(response[i].score).toFixed(2)+'</td>'+
    '<td>$'+response[i].a_eps+'</td>'+
    '<td>'+fyld+'</td>'+
    '</tr>';
  }
document.getElementById('stocksort').innerHTML=output;
};
}
run();
