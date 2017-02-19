function zoom_to_geojson(map, geojson){
  // Geographic coordinates of the LineString
  var coordinates = geojson.features[0].geometry.coordinates;

  // Pass the first coordinates in the LineString to `lngLatBounds` &
  // wrap each coordinate pair in `extend` to include them in the bounds
  // result. A variation of this technique could be applied to zooming
  // to the bounds of multiple Points or Polygon geomteries - it just
  // requires wrapping all the coordinates with the extend method.
  var bounds = coordinates.reduce(function(bounds, coord) {
      return bounds.extend(coord);
  }, new mapboxgl.LngLatBounds(coordinates[0], coordinates[0]));

  map.fitBounds(bounds, {
      padding: 20
  });
}
