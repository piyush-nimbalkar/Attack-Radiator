function loadJSON() {
    var data_file = "http://localhost:8000/data.json";
    var http_request = new XMLHttpRequest();
    // Opera 8.0+, Firefox, Chrome, Safari
    http_request = new XMLHttpRequest();
    http_request.onreadystatechange  = function() {
        if (http_request.readyState == 4) {
            var jsonObj = JSON.parse(http_request.responseText);
            if (jsonObj.processor_time > 11) {
                $("#processor_time").removeClass("green")
                $("#processor_time").addClass("red")
            }
            if (jsonObj.memory_usage > 11) {
                $("#memory_usage").removeClass("green")
                $("#memory_usage").addClass("red")
            }
            if (jsonObj.io_operations > 11) {
                $("#io_operations").removeClass("green")
                $("#io_operations").addClass("red")
            }
        }
    }
    http_request.open("GET", data_file, true);
    http_request.send();
}

$(document).ready(function() {
    loadJSON();
});
