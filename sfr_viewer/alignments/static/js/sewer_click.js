//highlight whats been clicked


function model_sewer_popup(map, feature, e){

  map.setFilter("sewer-hover", ["==", "Name", feature.properties.Name]);
  var props = feature.properties;
  var cap = props.MaxQ / props.MaxQPerc; //capacity
  var cost = "$" +(props.TotalCostEstimate / 1000000).toFixed(1) +"M";

  var html_message = [props.Name,
                      'Peak Flow: ' + props.MaxQ + 'cfs',
                      'Capacity: '+ Math.round(cap * 10) / 10 + 'cfs',
                      'Geom1: ' + props.Geom1,
                      'Geom2: ' + props.Geom2,
                      'Length: ' + props.Length + 'ft',
                      'Cost Estimate: ' + cost,
                      'Shape: '+ props.Shape,
                    ];

  var popup = new mapboxgl.Popup()
      .setLngLat(map.unproject(e.point))
      .setHTML(html_message.join('<br>'))
      .addTo(map);
}

function wwgrav_popup(map, feature, e){

  var props = feature.properties
  var html_message = [
                      'Type: '+ props.PIPE_TYPE,
                      'Height: ' + props.Height,
                      'Diameter: ' + props.Diameter,
                      'Material: '+ props.Material,
                      'Year: ' + props.Year_Insta,
                      '<a target="_blank" href="' + props.STICKERLIN + '">Sticker Link</a>',
                    ];

  var popup = new mapboxgl.Popup()
      .setLngLat(map.unproject(e.point))
      .setHTML(html_message.join('<br>'))
      .addTo(map);
}
