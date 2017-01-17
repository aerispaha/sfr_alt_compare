
// Set up the map
var mymap = L.map('map_wrapper').setView([39.921685, -75.148946], 15);
var tile_url = 'https://api.mapbox.com/styles/v1/mapbox/dark-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYWVyaXNwYWhhIiwiYSI6ImNpdWp3ZTUwbDAxMHoyeXNjdDlmcG0zbDcifQ.mjQG7vHfOacyFDzMgxawzw'
L.tileLayer(tile_url).addTo(mymap);
L.control.scale().addTo(mymap);

// POPUPS
function onEachFeature(feature, layer) {
// does this feature have a property named popupContent?
console.log(feature.properties.RealGeom1)
// console.log(layer)
    if (feature.properties) {
      if (feature.properties.Shape != 'CIRCULAR' & feature.properties.RealGeom1 & feature.properties.RealGeom2){
        size = feature.properties.RealGeom1.toFixed(1) + 'ft x ' + feature.properties.RealGeom2.toFixed(1) + 'ft ';
      }else {
        size = feature.properties.RealGeom1 +'ft '
      };
        size += feature.properties.Shape
        id = feature.properties.InletNode;
        cost_raw = feature.properties.TotalCostEstimate;
        cost = '$' + Number(cost_raw.toFixed(1)).toLocaleString();
        length = Math.round((feature.properties.Length / 5280) * 100)/100 + ' miles'
        popupContent = [id, size, length, cost].join('<br>');
        // layer.bindPopup('Geom1 % ' + feature.properties.MaxQPercent);
        layer.bindPopup(popupContent);
    };

}
// ADD THE DATA TO MAP, zoom to the bounds
features = L.geoJSON(data, {onEachFeature:onEachFeature, style:{"weight":5}}).addTo(mymap);
// mymap.fitBounds(features.getBounds());

if (data2){
  // HOJCOJODJEOJODEJD
  var diffstyle = {
    //#4caf5
    "color": "#009688",
    "weight": 5,
};
  L.geoJSON(data2, {onEachFeature:onEachFeature, style:diffstyle}).addTo(mymap);
}
