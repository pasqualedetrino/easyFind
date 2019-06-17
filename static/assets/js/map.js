var map = L.map('map').fitWorld();
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.streets'
}).addTo(map);
var pos;
var geocodeService = L.esri.Geocoding.geocodeService();

function onLocationFound(e) {
	var radius = e.accuracy / 2;
	pos = e.latlng;
	geocodeService.reverse().latlng(e.latlng).run(function(error, result) {
      L.marker(result.latlng).addTo(map).bindPopup(result.address.Match_addr).openPopup();
		document.getElementById("indirizzo").value = result.address.Address+", "+result.address.Postal;
		document.getElementById("Citta").value = result.address.City;
    });

	document.getElementById("lat").value = pos.lat;

	document.getElementById("long").value = pos.lng;
}


function onLocationError(e) {
    e.message = "Impossibile usufruire del servizio senza attivare la posizione GPS!"
    alert(e.message);
}

map.locate({setView: true, maxZoom: 16});

map.on('locationfound', onLocationFound);
map.on('locationerror', onLocationError);
