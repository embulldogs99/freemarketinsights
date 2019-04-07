function correlation(){
    var client=new XMLHttpRequest();
    client.open("Get","/json/correlations.json",true);
    client.send();
    client.onreadystatechange=function(){
      var response=JSON.parse(client.responseText);

      var output='';
      var dates=[];
      var gold=[];
      var spx=[];
      var goldcum=[];
      var spxcum=[];
      for (var i=0;i<obj.data.length;i++){

            dates.push(obj.data[i][0]);
            gold.push(obj.data[i][1]);
            spx.push(obj.data[i][2]);
            goldcum.push(obj.data[i][3]);
            spxcum.push(obj.data[i][4]);

        }
      }
}
