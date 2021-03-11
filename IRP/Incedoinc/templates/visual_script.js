google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

document.addEventListener('DOMContentLoaded', () =>{
  // document.querySelector('#pie_chart_req').innerHTML
  drawChart();
});
function drawChart() {
  var data = google.visualization.arrayToDataTable([
  ['Task', 'Hours per Day'],
]);

  // Optional; add a title and set the width and height of the chart
  var options = {'title':'My Average Day', 'width':550, 'height':400};

  // Display the chart inside the <div> element with id="piechart"
  var chart = new google.visualization.PieChart(document.getElementById('piechart'));
  chart.draw(data, options);
}
