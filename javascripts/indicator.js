function loadJSON() {
    var data_file = "http://localhost:8000/data.json";
    var http_request = new XMLHttpRequest();
    // Opera 8.0+, Firefox, Chrome, Safari
    http_request = new XMLHttpRequest();
    http_request.onreadystatechange  = function() {
        if (http_request.readyState == 4) {
            var jsonObj = JSON.parse(http_request.responseText);
            $("#processor_time .label").append("(" + jsonObj.processor_time.toFixed(2) + ")");
            $("#memory_usage .label").append("(" + jsonObj.memory_usage.toFixed(2) + ")");
            $("#io_operations .label").append("(" + jsonObj.io_operations.toFixed(2) + ")");
            $("#packet_frequency .label").append("(" + jsonObj.packet_frequency.toFixed(2) + ")");

            if (jsonObj.processor_time > 2.5) {
                $("#processor_time").removeClass("green");
                $("#processor_time").addClass("red");
            }
            if (jsonObj.memory_usage > 36659200) {
                $("#memory_usage").removeClass("green");
                $("#memory_usage").addClass("red");
            }
            if (jsonObj.io_operations > 1100) {
                $("#io_operations").removeClass("green");
                $("#io_operations").addClass("red");
            }
            if (jsonObj.packet_frequency > 1) {
                $("#packet_frequency").removeClass("green");
                $("#packet_frequency").addClass("red");
            }
            if (jsonObj.dll_list.length > 0) {
                $("#dll").removeClass("green");
                $("#dll").addClass("red");
                $("#dll_list").addClass("red");
                $("#dll_list").html(dll_list(jsonObj.dll_list));
            }
        }
    }
    http_request.open("GET", data_file, true);
    http_request.send();
}

function dll_list(list) {
    var str = "<div>SUSPICIOUS DLLs</div><ul>";
    for (var i = 0; i < list.length; i++) {
        str = str +  "<li>" + list[i] + "</li>";
    }
    str = str + "</ul>";
    return str;
}

$(document).ready(function() {
    loadJSON();
});
