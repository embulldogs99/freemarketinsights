
function run(){
var client=new XMLHttpRequest();
client.open("Get","/json/goldpricez.json",true);
client.send();
client.onreadystatechange=function(){
var response=JSON.parse(client.responseText);
var oldusgold=response.T1.ounce_price_usd;
var newusgold=response.T.ounce_price_usd;
var goldchange=parseFloat(((newusgold-oldusgold)/oldusgold*100).toFixed(3));
var oldspxtogold=response.T1.spx_gold;
var newspxtogold=response.T.spx_gold;
var spxtogoldchange=parseFloat(((newspxtogold-oldspxtogold)/oldspxtogold*100).toFixed(3));
var goldchangeimage='';
if (goldchange>0){
  goldchangeimage+='<div class="green_arrow"></div>';
}else if (goldchangeimage<0){
  goldchangeimage+='<div class="red_arrow"></div>';
}else {
  goldchangeimage+='<div class="nochange"></div>';
}

var spxgoldchangeimage='';
if (spxtogoldchange>0){
  spxgoldchangeimage+='<div class="green_arrow"></div>';
} else if (spxtogoldchange<0){
  spxgoldchangeimage+='<div class="red_arrow"></div>';
} else{
  spxgoldchangeimage+='<div class="nochange"></div>';
}
var output='';
output+='<tr>'+
'<td><a href="/research/gold"><td class="goldimage"></td></a>'+
'<td>$'+newusgold+'</td>'+
'<td>'goldchange+'%</td>'+
'<td>'+goldchangeimage+'</td>'+
'<td>SPX/G</td>'+
'<td>'+newspxtogold+'</td>'+
'<td>'+spxtogoldchange+'%</td>'+
'<td>'+spxgoldchangeimage+'</td>'+
'</tr>';

    document.getElementById('goldtable').innerHTML=output;
};
}

run();
