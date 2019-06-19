var map = L.map('map').setView([40.87,14.29],16);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors ' +
        ' | Geocoder with <a href="https://github.com/perliedman/leaflet-control-geocoder">leaflet-control-geocoder</a> and <a href="https://operations.osmfoundation.org/policies/nominatim/">Nominatim</a> '
}).addTo(map);
var pos;
var geocodeService = L.Control.Geocoder.nominatim();
var gpsResult;
var mapResult;

var risultato = new L.LayerGroup().addTo(map);

var radius;
var flag = false;


function onLocationFound(e) {
    radius = e.accuracy;
    sleep(1500);
    console.log(e.latlng);
    risultato.clearLayers();
    geocodeService.reverse(e.latlng, map.options.crs.scale(16),function(result){
	    gpsResult=result[0];
	    console.log(gpsResult)
        if(gpsResult.properties.address.road !== undefined || gpsResult.properties.address.pedestrian !==  undefined) {
            risultato.addLayer(L.marker([gpsResult.properties.lat, gpsResult.properties.lon]).addTo(map).bindPopup(gpsResult.html).openPopup());
            risultato.addLayer(L.circle([gpsResult.properties.lat, gpsResult.properties.lon], radius).addTo(map));
             var ind = (gpsResult.properties.address.road || gpsResult.properties.address.pedestrian);
             if (gpsResult.properties.address.postcode !== undefined)
                 ind += ", " + gpsResult.properties.address.postcode;
            document.getElementById("indirizzo").value = ind;
            document.getElementById("Citta").value = (gpsResult.properties.address.city || gpsResult.properties.address.town);
            document.getElementById("lat").value = gpsResult.properties.lat;
            document.getElementById("long").value = gpsResult.properties.lon;
            flag = true;
        }

    });
}


function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}


  map.on('click', function(e)
  {
        sleep(1500);
        risultato.clearLayers();
    geocodeService.reverse(e.latlng, map.options.crs.scale(map.getZoom()),function(result){
	    mapResult=result[0];
        if(mapResult.properties.address.road !== undefined || mapResult.properties.address.pedestrian !==  undefined) {
            risultato.addLayer(L.marker([mapResult.properties.lat, mapResult.properties.lon]).addTo(map).bindPopup(mapResult.html).openPopup());
             var ind = (mapResult.properties.address.road || mapResult.properties.address.pedestrian);
             if (mapResult.properties.address.postcode !== undefined)
                 ind += ", " + mapResult.properties.address.postcode;
            document.getElementById("indirizzo").value = ind;
            document.getElementById("Citta").value = mapResult.properties.address.city;
            document.getElementById("lat").value = mapResult.properties.lat;
            document.getElementById("long").value = mapResult.properties.lon;
            if(flag === true) {
                document.getElementById("gps").innerHTML = "\t\t\t\t                        <button type=\"button\" style=\"margin-bottom: 7px\" onclick=\"ongps()\" class=\"btn\">Usa i dati gps</button>\n";
                document.getElementById("mappa").innerHTML = "\t\t\t\t                        <button type=\"button\" style=\"margin-bottom: 7px\" onclick='onmap()' class=\"btn\">Usa i dati dalla mappa</button>\n";
            }
        }

    });
  });


function onLocationError(e) {
    e.message = "Impossibile usufruire del servizio GPS!"
    document.getElementById("usaMappa").innerHTML = "GPS disabilitato, indicare la propria attività sulla mappa per completare la registrazione:";
    alert(e.message);
}

map.locate({setView: true, maxZoom: 16});

map.on('locationfound', onLocationFound);
map.on('locationerror', onLocationError);


function onmap()
{
                 var ind = (mapResult.properties.address.road || mapResult.properties.address.pedestrian);
             if (mapResult.properties.address.postcode !== undefined)
                 ind += ", " + mapResult.properties.address.postcode;
            document.getElementById("indirizzo").value = ind;
            document.getElementById("Citta").value = mapResult.properties.address.city;
            document.getElementById("lat").value = mapResult.properties.lat;
            document.getElementById("long").value = mapResult.properties.lon;
}


function ongps()
{
                 var ind = (gpsResult.properties.address.road || gpsResult.properties.address.pedestrian);
             if (gpsResult.properties.address.postcode !== undefined)
                 ind += ", " + gpsResult.properties.address.postcode;
            document.getElementById("indirizzo").value = ind;
            document.getElementById("Citta").value = gpsResult.properties.address.city;
            document.getElementById("lat").value = gpsResult.properties.lat;
            document.getElementById("long").value = gpsResult.properties.lon;
}

