// 
function ajax_fillTable(id) {
  $.ajax({ type: "GET", dataType: "json", url: "/api/" + id + "/TempCs",
    success: function(data) {
      // foreach entry
      var index;
      console.log("data result length: " + data.result.length);
      for (index = 0; index < data.result.length; ++index) {
        //console.log("index: " + index);
        var date = new Date(data.result[index].timestamp * 1000);
        //var datetime = date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds() + " " + date.getDay() + "/" + date.getMonth() + "/" + date.getFullYear();
        var datetime = date.toDateString() + " " + date.toTimeString() ;
        var entry = "<tr class=\"gradeA\"><td>" + datetime + "</td><td>" + data.result[index].tempC + " C</td></tr>";
        $("#dataTable > tbody:last").append(entry);
      }
    }});
}
 
function ajax_lastTempC(id) {
  $.ajax({ type: "GET", dataType: "json", url: "/api/" + id + "/TempCs",
    success: function(data) {
      $("#" + id + "_lastTempC").text(data.result[0].tempC + " C");
    }});
}

