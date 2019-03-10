
function run(){
var client=new XMLHttpRequest();
client.open("Get","/json/goldpricez.json",true);
client.send();
client.onreadystatechange=function(){
var response=JSON.parse(client.responseText);
var oldusgold=response['T1']['ound_price_usd'];
var newusgold=response['T']['ound_price_usd'];
var goldchange=(newusgold-oldusgold)/oldusgold;
var oldspxtogold=response['T1']['spx/gold'];
var newspxtogold=response['T']['spx/gold'];
var spxtogoldchange=(newspxtogold-oldspxtogold)/oldspxtogold;
var output='';
output+='<tr>'+
'<td>Gold Price USD</td>'+
'<td>'+newusgold+'</td>'+
'<td>Gold Price Change:'+'</td>'+
'<td>'+goldchange+'</td>'+
'<td>SPX to Gold Ratio</td>'+
'<td>'+newspxtogold+'</td>'+
'<td>SPX to Gold Ratio Change %:</td>'+
'<td>'+spxtogoldchange+'</td>'+
'</tr>';
}
document.write(output);

}

run();