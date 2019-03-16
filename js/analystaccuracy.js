function metastats(){

  var xhttp=new XMLHttpRequest();
  xhttp.open('Get','/json/historicalanalysis/historicalanalysisstats.json');
  xhttp.send();
  xhttp.onreadystatechange=function(){
    if (this.readyState==4 && this.status==200){
      var response=JSON.parse(xhttp.responseText);
      metastats='';
      metastats+='In our most recent data pull on '+response.DateRun+', we surveyed '+response.StockCount+' different analyst target prices from before '+response.PullDate+'.  Of those predictions, '+(response.PercentBull*100)toFixed(2)+'% where bullish and '+(response.PercentBear*100).toFixed(2)+'% where bearish.<br><br> Of those predictions, '+(response.PercentCall*100).toFixed(2)+' predicted the future stock price direction correctly. One average the actual stock return was '+(response.AvgReturn*100).toFixed(2)+'% while the average expected return was '+(response.AvgExpectedReturn).toFixed(2)+'%. On average, the analysts missed their prediction by '+(response.AvgReturnDelta*100).toFixed(2)+'%.<br><br> These results are often staggering. There are many factors that could explain these results such as macro-economic trends, analyst bias, analyst confidence, and others. We continue to run this analysis from time to time to see if the results change under different environmental conditions. However, regardless of the average results, this data always begs the question: Which Analysts did the best?'

      document.getElementById('metastats').innerHTML=metastats;

    }
  };
}


function bankstats(){

  var xhttp=new XMLHttpRequest();
  xhttp.open('Get','/json/historicalanalysis/historicalanalysisstats.json');
  xhttp.send();
  xhttp.onreadystatechange=function(){
    if (this.readyState==4 && this.status==200){
      var response=JSON.parse(xhttp.responseText);
      var data=response.data;
      output='<tr><th>Bank</th><th>Prediction</th><th>Avg Actual Return</th><th>Avg Expected Return</th><th>Average Return Delta</th></tr>';
      for (i=0;i<data.length;i++){
        output+='';
      }
      document.getElementById('bankstats').innerHTML=output;
    }
  };
}

metastats();
bankstats();
