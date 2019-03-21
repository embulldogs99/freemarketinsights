function metastats(){

  var xhttp=new XMLHttpRequest();
  xhttp.open('Get','/json/historicalanalysis/historicalanalysisstats.json');
  xhttp.send();
  xhttp.onreadystatechange=function(){
    if (this.readyState==4 && this.status==200){
      var response=JSON.parse(xhttp.responseText);
      console.log(response);
      metastats='';
      metastats+='In our most recent data pull on '+response[0].DateRun+', we surveyed '+response[0].StockCount+' different analyst target prices from before '+response[0].PullDate;
      metastats+='.  Of those predictions, '+(response[0].PercentBull*100).toFixed(2)+'% where bullish and '+(response[0].PercentBear*100).toFixed(2)+'% where bearish.<br><br> Of those predictions, ';
      metastats+=parseFloat(response[0].PercentCall*100).toFixed(2)+' predicted the future stock price direction correctly. One average the actual stock return was '+parseFloat(response[0].AvgReturn*100).toFixed(2)+'% while the average expected return was '+parseFloat(response[0].AvgExpectedReturn).toFixed(2)+'%. On average, the analysts missed their prediction by '+parseFloat(response[0].AvgReturnDelta*100).toFixed(2);
      metastats+='%.<br><br> These results are often staggering. There are many factors that could explain these results such as macro-economic trends, analyst bias, analyst confidence, and others. We continue to run this analysis from time to time to see if the results change under different environmental conditions. However, regardless of the average results, this data always begs the question: Which Analysts did the best?';

      document.getElementById('metastats').innerHTML=metastats;

    }
  };
}


function bankstats(){

  var xhttp=new XMLHttpRequest();
  xhttp.open('Get','/json/historicalanalysis/bankanalysis.json');
  xhttp.send();
  xhttp.onreadystatechange=function(){
    if (this.readyState==4 && this.status==200){
      var response=JSON.parse(xhttp.responseText);
      var data=response.data;
      console.log(data);
      output='<tr><th>Bank</th><th>Prediction</th><th>Avg Actual Return</th><th>Avg Expected Return</th><th>Average Return Delta</th><th>Target Prices Analyzed</th><th>Accuracy</th></tr>';
      for (i=0;i<data.length;i++){
        output+='<tr>'+
        '<td>'+data[i].bank+'</td>'+
        '<td>'+data[i].prediction+'</td>'+
        '<td>'+data[i].act_return+'</td>'+
        '<td>'+data[i].exp_return+'</td>'+
        '<td>'+data[i].ret_delta+'</td>'+
        '<td>'+data[i].rowcount+'</td>'+
        '<td>'+(data[i].accuracy*100).toFixed(2)+'%</td>'+
        '</tr>';
      }
      document.getElementById('bankstats').innerHTML=output;
    }
  };
}

metastats();
bankstats();
