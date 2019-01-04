var map
var latLngStack = []
var renderedStack = []

var tipi = {lat: 52.0799122, lng: 4.5056178};

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

//  Function:
//  registerEventListenersOnMap()
//  Renders the list of lat lng coordinates on the map.
function registerEventListenersOnMap() {
    google.maps.event.addListener(map, 'click', function(event) {
        latLngStack.push(event.latLng);
        console.log(latLngStack)
    });
}

function renderStackOnMap(map) {
  for (elemIndex in latLngStack) {
    console.log(tipi);
    renderedStack.push(new google.maps.Marker({
      position: latLngStack[elemIndex],
      map: map
    }));
  }
}

function initMap(){
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    center: tipi
  });
  registerEventListenersOnMap();
}

$(document).ready(function(){
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        var csrftoken = getCookie("csrftoken");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  $("#reset").click(function(event) {
    latLngStack.length = 0;
    while (elem = renderedStack.pop()) {
      elem.setMap(null);
    }
  });
  $("#render").click(function(event) {
    renderStackOnMap(map);
  });
  $("#submit").click(function(event) {
    console.log(tipi, JSON.stringify(latLngStack));

    $.post("/dev/add_track/",
    {
        tipi: tipi,
        stack: JSON.stringify(latLngStack)
    },
    function(data, status) {
      console.log("Data: " + data + "\nStatus: " + status);
    });
  });
});
