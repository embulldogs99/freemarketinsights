


// jQuery
$.getScript('/js/papaparse.js', function()
{




  var client=new XMLHttpRequest();
  client.open("Get","/csv/spxvsgoldata.csv",true);
  client.send();
  client.onreadystatechange=function(){
    var obj=Papa.parse(client.responseText);

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




      var ctx = document.getElementById('myChart').getContext('2d');
          var myLineChart = new Chart(ctx, {
          type: 'line',
          data:{
            labels:dates,
            datasets:[{
              label:"Gold",
              backgroundColor: 'rgba(0,0,0,0)',
              borderColor: 'rgb(255, 99, 132)',
              data:gold,
            },{
              label:"SPX",
              backgroundColor: 'rgba(0,0,0,0)',
              borderColor: 'rgb(0, 99, 0)',
              data:spx,
            }]

          },

          options:{}
      });




            var ctx2 = document.getElementById('mycumChart').getContext('2d');
                var myLineChart = new Chart(ctx2, {
                type: 'line',
                data:{
                  labels:dates,
                  datasets:[{
                    label:"Gold Cumulative Return",
                    backgroundColor: 'rgba(0,0,0,0)',
                    borderColor: 'rgb(255, 99, 132)',
                    data:goldcum,
                  },{
                    label:"SPX Cumulative Return",
                    backgroundColor: 'rgba(0,0,0,0)',
                    borderColor: 'rgb(0, 99, 0)',
                    data:spxcum,
                  }]

                },

                options:{}
            });


    document.getElementById('goldata').innerHTML=dates;
  };



});
