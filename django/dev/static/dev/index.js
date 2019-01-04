

var HuntedClient = {}
(function(context) {
  // Constants
  var WaypointRequestURL = '/dev/waypoints';
  var WaypointSubmitURL = '/dev/waypoints';
  var LocationRequestURL = '/dev/locations';
  var LocationSubmitURL = '/dev/locations';

  // Variables
  var map;

  var waypointData = [];
  var renderedWaypoints = [];
  var locationData = [];
  var renderedLocations = [];

  requestWaypointData = function() {
    waypointData = [];
    $.get(WaypointRequestURL, function(data, status) {
      jsonData = JSON.parse(data);
      for (waypointIndex in jsonData) {
        data = jsonData[waypointIndex].fields;
        waypointData.push({
          lat: data.lat,
          lng: data.lon,
          value: data.value
        });
      }
    });
  }

  requestLocationData = function() {
    locationData = [];
    $.get(LocationRequestURL, function(data, status) {
      jsonData = JSON.parse(data);
      for (locationIndex in jsonData) {
        data = jsonData[waypointIndex].fields;
        waypointData.push({
          lat: data.lat,
          lng: data.lon,
          value: data.value
        });
      }
    });
  }

  submitLocationData = function(location) {

    data = {lat: location.coords.latitude,
            lng: location.coords.longitude,
            acc: location.coords.accuracy};

    $.post(LocationSubmitURL, data, function() {
      console.log("Lat: " + lat + "\nLng: " + lng + "\nAcc: " + acc)
    });
  }

})(HuntedClient);




var map
var renderedWaypoints;
var renderedLocations;

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


function renderWaypointsOnMap(map, waypoints) {
  var renderedWaypoints = [];
  for (waypointIndex in waypoints) {
    if (waypoints.score < 10) {
      iconFilename = '/static/dev/blue_MarkerA.png';
    } else if (waypoints.score < 20) {
      iconFilename = '/static/dev/darkgreen_MarkerA.png';
    } else if (waypoints.score < 30) {
      iconFilename = '/static/dev/green_MarkerA.png';
    } else if (waypoints.score < 40) {
      iconFilename = '/static/dev/yellow_MarkerA.png';
    } else if (waypoints.score < 50) {
      iconFilename = '/static/dev/orange_MarkerA.png';
    } else {
      iconFilename = '/static/dev/red_MarkerA.png';
    }
    renderedWaypoints.push(new google.maps.Marker({
      position: waypoints[waypointIndex],
      map: map,
      icon: iconFilename
    }));
  }
  console.log("Rendered waypoints on map.");
  return renderedWaypoints;
}


function registerEventListenersOnMap(map) {

  google.maps.event.addListenerOnce(map, 'idle', function() {
    // Get the waypoints once. Selection is done serverside. Todo: inside permission check.
    waypointData = [];
    $.get("/dev/waypoints", function(data, status) {
      jsonData = JSON.parse(data);
      for (waypointIndex in jsonData) {
        data = jsonData[waypointIndex].fields;
        waypointData.push({
          lat: data.lat,
          lng:data.lon,
          score:data.score
        });
      }
      renderedWaypoints = renderWaypointsOnMap(map, waypointData);
    });

    // Send the location every 10 seconds
    if (navigator.geolocation) {
      window.setInterval(function() {
        navigator.geolocation.getCurrentPosition(function(pos) {
          lat = pos.coords.latitude;
          lng = pos.coords.longitude;
          acc = pos.coords.accuracy;

          $.post("/dev/locations",
            {
              lat: lat,
              lon: lng,
              acc: acc
            },
            function() {
              console.log("Lat: " + lat + "\nLng: " + lng + "\nAcc: " + acc);
            });
        },
        function error(msg) {
          alert("Please enable your GPS position.\nNo GPS, no GPS game.");
        },
        {timeout: 10000, maximumAge: 0, enableHighAccuracy: true});
      }, 10000);
    } else {
      // Die gracefully. No GPS, no GPS game.
      console.log("No location service available.")
    }

    // Update each 20 sec
    window.setInterval(function() {
      locationData = [];
      $.get("/dev/locations", function(data, status) {
        jsonData = JSON.parse(data);
        for (locationIndex in jsonData) {
          data = jsonData[locationIndex];
          locationData.push({
            lat: data.lat,
            lng: data.lon,
            score: 50
//            score:data.score  // Not score, but something else, like team cachable or not.
          });
        }
        renderedLocations = renderWaypointsOnMap(map, locationData);
      })
    }, 20000);
  });
}


function initMap(){
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    center: {lat: 52.083508, lng: 4.507568}
  });
  registerEventListenersOnMap(map);
}


$(document).ready(function() {

  console.log("Document ready fired.");
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        var csrftoken = getCookie("csrftoken");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
});
