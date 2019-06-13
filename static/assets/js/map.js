var map = L.map('map').fitWorld();
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.streets'
}).addTo(map);
var pos;

function onLocationFound(e) {
	var radius = e.accuracy / 2;
	pos = e.latlng;
	L.marker(e.latlng).addTo(map)
		.bindPopup("You are within " + radius + " meters from this point").openPopup();
	/*html = "\t\t\t\t                        \t<label class=\"sr-only\" for=\"form-about-yourself\">Latitudine</label>\n" +
		"                                            <input title=\"Longitudine: Acquisita tramite posizione GPS\" type=\"text\" name=\"lat\" placeholder=\"Latitudine...\" class=\"form-control\" id=\"lat\" value=\""+pos.lat+"\" disabled required>";*/
	document.getElementById("lat").value = pos.lat;

	 /*html = "\t\t\t\t                        \t<label class=\"sr-only\" for=\"form-about-yourself\">Longitudine</label>\n" +
		"                                            <input title=\"Latitudine: Acquisita tramite posizione GPS\" type=\"text\" name=\"long\" placeholder=\"Longitudine...\" class=\"form-control\" id=\"long\"  value=\""+pos.lng+"\" disabled required>";*/
	document.getElementById("long").value = pos.lng;
}


function onLocationError(e) {
    e.message = "Impossibile usufruire del servizio senza attivare la posizione GPS!"
    alert(e.message);
}

map.locate({setView: true, maxZoom: 16});

map.on('locationfound', onLocationFound);
map.on('locationerror', onLocationError);