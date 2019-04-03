

function mbear(){
var xhttp2=new XMLHttpRequest();
xhttp2.onreadystatechange=function(){
  if (this.readyState ==4 && this.status ==200){
    var response2=JSON.parse(xhttp2.responseText);
    var output2='';
    for (var i=0;i<5;i++){
      if (response2[i].divyield==null){divyield="-";}else{divyield=response2[i].divyield;}

	output2 +=
		'<div style="justify-content:space-between;">' +
		'<div id="countNumbers">0'+(parseFloat(i)+1)+'</div>'+
		'<a href="http://www.google.com/search?q='+response2[i].ticker+'+stock+price"  target="_blank" >'+response2[i].ticker+'</a>'+
		'<br>'+
		'<a href="http://www.google.com/search?q='+response2[i].note+'"  target="_blank" >'+response2[i].note+'</a></td>'+
		'<br>'+
		'<b class="text-dark">'+'Last Price:$'+response2[i].price+'</b>'+
		'<b class="text-dark">'+'Expected Return:'+response2[i].returns+'%'+'</b>'+
		'<b class="text-dark">'+'Dividend Yield:'+divyield+'% </b>'+
		'<br>' +
		'<br>' +
		'</div>';
    }

    document.getElementById('mbear').innerHTML=output2;
    }
  };
  xhttp2.open("Get", "json/marketbears.json",true);
  xhttp2.send();
}

function portfoliochart(){

  var xhttp3=new XMLHttpRequest();
  xhttp3.onreadystatechange=function(){
    if (this.readyState ==4 && this.status ==200){
      var response3=JSON.parse(xhttp3.responseText);
      var snp=[1];
      var port=[1];
      var nas=[1];
      var oldsnp=0;
      var labels=["$1"];
      for (var i=0;i<response3.length;i++){
        if(i==0){
          oldsnp=1+response3[i].snpreturn;
          oldnas=1+response3[i].nasdaqreturn;
          oldport=1+response3[i].portfolioreturn;
          snp.push((1+Number(response3[i].snpreturn)).toFixed(3));
          nas.push((1+Number(response3[i].nasdaqreturn)).toFixed(3));
          port.push((1+Number(response3[i].portfolioreturn)).toFixed(3));
          labels.push(response3[i].to_char);
        }else{
          snp.push((oldsnp+Number(oldsnp)*response3[i].snpreturn).toFixed(3));
          nas.push((oldnas+Number(oldnas)*response3[i].nasdaqreturn).toFixed(3));
          port.push((oldport+Number(oldport)*response3[i].portfolioreturn).toFixed(3));
          labels.push(response3[i].to_char);
          oldsnp=Number(oldsnp)+Number(oldsnp)*response3[i].snpreturn;
          oldnas=Number(oldnas)+Number(oldnas)*response3[i].nasdaqreturn;
          oldport=Number(oldport)+Number(oldport)*response3[i].portfolioreturn;
        }

      }
  var ctx = document.getElementById('myChart').getContext('2d');
      var myLineChart = new Chart(ctx, {
      type: 'line',
      data:{
        labels:labels,
        datasets:[{
          label:"SnP 500",
          backgroundColor: 'rgba(0,0,0,0)',
          borderColor: 'rgb(255, 99, 132)',
          data:snp,
        },{
          label:"Nasdaq",
          backgroundColor: 'rgba(0,0,0,0)',
          borderColor: 'rgb(0, 99, 0)',
          data:nas,
        },{
          label:"FMI Portfolio",
          backgroundColor: 'rgba(0,0,0,.2)',
          borderColor: 'rgb(0, 128, 128)',
          data:port,
        }]

      },

      options:{
          title:{
            display:true,
            text:'Cumulative Return vs Benchmark'
          }
      }
  });

    }
  };
  xhttp3.open("Get", "json/portfoliohistory.json",true);
  xhttp3.send();
}



function golddata(){
var client=new XMLHttpRequest();
client.open("Get","/json/goldpricez.json",true);
client.send();
client.onreadystatechange=function(){
var response=JSON.parse(client.responseText);
var oldusgold=response.T1[0].ounce_price_usd;
var newusgold=response.T[0].ounce_price_usd;
var goldchange=parseFloat(((newusgold-oldusgold)/oldusgold*100).toFixed(3));
var oldspxtogold=response.T1[0].spx_gold;
var newspxtogold=response.T[0].spx_gold;
var spxtogoldchange=parseFloat(((newspxtogold-oldspxtogold)/oldspxtogold*100).toFixed(3));

var goldchangeimage='';
if (goldchange>0){goldchangeimage=' class="green_arrow"';}
if (goldchange<0){goldchangeimage=' class="red_arrow"';}
if (goldchange==0){goldchangeimage=' class="nochange"';}

var spxgoldchangeimage='';
if (spxtogoldchange>0){spxgoldchangeimage=' class="green_arrow"';}
if (spxtogoldchange<0){spxgoldchangeimage=' class="red_arrow"';}
if (spxtogoldchange==0){spxgoldchangeimage=' class="nochange"';}

var output='';
output+='<tr>'+
'<a href="/research/gold"><td class="goldimage">'+newusgold+'<br>'+goldchange+'%<br><div '+goldchangeimage+'></div></td></a></tr><tr>'+
'<td>SPX/G<br>'+newspxtogold+'<br>'+spxtogoldchange+'%<br><div '+spxgoldchangeimage+'></div></td>'+
'</tr>';

    document.getElementById('goldtable').innerHTML=output;
};
}

function mbull(){
var xhttp=new XMLHttpRequest();
xhttp.onreadystatechange=function(){
  if (this.readyState ==4 && this.status ==200){

    var response=JSON.parse(xhttp.responseText);

    var output='';
    for (var i=0;i<5;i++){
      if (response[i].divyield==null){divyield="-";}else{divyield=response[i].divyield;}
		output +=
			'<div style="justify-content:space-between;">' +
			'<div>0'+(parseFloat(i)+1)+'</div>'+
			'<a href="http://www.google.com/search?q='+response[i].ticker+'+stock+price"  target="_blank" >'+response[i].ticker+'</a>'+
			'<br>'+
			'<a href="http://www.google.com/search?q='+response[i].note+'"  target="_blank" >'+response[i].note+'</a></td>'+
			'<br>'+
			'<b class="text-dark">'+'Target:$'+response[i].target+' </b>'+
			'<b class="text-dark">'+'Price:$'+response[i].price+' </b>'+
			'<b class="text-dark">'+'Expected Return:'+response[i].returns+'%'+'</b>'+
			'<b class="text-dark">'+'Dividend Yield:'+divyield+'% </b>'+
			'<br>' +
			'<br>' +
			'</div>';
    }

    document.getElementById('mbull').innerHTML=output;
    }
  };
  xhttp.open("Get", "json/marketbulls.json",true);
  xhttp.send();
}


mbull();
golddata();
portfoliochart();
mbear();
