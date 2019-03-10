
function run(){
var client=new XMLHttpRequest();
client.open("Get","/json/goldpricez.json",true);
client.send();
console.log(client.responseText);
client.onreadystatechange=function(){
var response=JSON.parse(client.responseText);
var oldusgold=response.T1[0].ounce_price_usd;
var newusgold=response.T[0].ounce_price_usd;
var goldchange=(newusgold-oldusgold)/oldusgold;
var oldspxtogold=response.T1[0].spx_gold;
var newspxtogold=response.T[0].spx_gold;
var spxtogoldchange=(newspxtogold-oldspxtogold)/oldspxtogold;
if (goldchange>0){
  var goldchangeimage='<img src="/pics/green_arrow.png" height="50" width="50"/>';
}else if (goldchangeimage<0){
  goldchangeimage='<img src="/pics/red_arrow.png" height="50" width="50"/>';
}else {
  goldchangeimage='<img src="/pics/nochange.png" height="50" width="50"/>';
}

if (spxtogoldchange>0){
  spxgoldchangeimage='<img src="/pics/green_arrow.png" height="50" width="50"/>';
} else if (spxtogoldchange<0){
  spxgoldchangeimage='<img src="/pics/red_arrow.png" height="50" width="50"/>';
} else{
  spxgoldchangeimage='<img src="/pics/nochange.png" height="50" width="50"/>';
}
var output='';
output+='<tr>'+
'<a href="/research/gold"><td class="goldimage"></a><br><font style="font-weight:900;"$'+newusgold+'</font></td>'+
'<td>'+goldchangeimage+goldchange+'%</td>'+
'<td>SPX to Gold Ratio</td>'+
'<td>'+newspxtogold+'</td>'+
'<td>'+spxgoldchangeimage+spxtogoldchange+'%</td>'+
'</tr>';

    document.getElementById('goldtable').innerHTML=output;
    conole.log(output);
};
}

run();
