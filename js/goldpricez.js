
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
  var goldchangeimage='<div class="green_arrow"></div>';
}else if (goldchangeimage<0){
  goldchangeimage='<div class="red_arrow"></div>';
}else {
  goldchangeimage='<div class="nochange"></div>';
}

if (spxtogoldchange>0){
  spxgoldchangeimage='<div class="green_arrow"></div>';
} else if (spxtogoldchange<0){
  spxgoldchangeimage='<div class="red_arrow"></div>';
} else{
  spxgoldchangeimage='<div class="nochange"></div>';
}
var output='';
output+='<tr>'+
'<td><a href="/research/gold"><div class="goldimage"></div></a><font style="font-weight:900;"$'+newusgold+'</font></td>'+
'<td>'+goldchangeimage+goldchange+'%</td>'+
'<td>SPX to Gold Ratio <br>'+newspxtogold+'</td>'+
'<td>'+spxgoldchangeimage+spxtogoldchange+'%</td>'+
'</tr>';

    document.getElementById('goldtable').innerHTML=output;
    conole.log(output);
};
}

run();
