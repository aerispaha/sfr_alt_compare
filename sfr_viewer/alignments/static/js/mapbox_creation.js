mapboxgl.accessToken = 'pk.eyJ1IjoiYWVyaXNwYWhhIiwiYSI6ImNpdWp3ZTUwbDAxMHoyeXNjdDlmcG0zbDcifQ.mjQG7vHfOacyFDzMgxawzw';
var map = new mapboxgl.Map({
    style:'mapbox://styles/aerispaha/cizbpt6w9001b2so3hi3kvfkr',//'mapbox://styles/mapbox/dark-v9',
    center: [-75.1546054, 39.9195164],
    zoom: 14,
    //pitch: 20,
    //bearing: -17.6,
    container: 'map_wrapper',
});


//INSERT GEOJSON HERE ~~~~~
var sewer_source, parcel_source;
$('.button').click(function() {
  var pth = $(this).data('path')
  console.log(pth);

  $.get(pth, function (newdata) {
        map.getSource('sewer-data').setData(newdata);
    });
});
var geocoder;
map.on('load', function() {

  //add a geocoder to the map
  geocoder = new MapboxGeocoder({accessToken: mapboxgl.accessToken});
  map.addControl(geocoder);

  //load the data into the map
  sewer_source = map.addSource('sewer-data', {'type': 'geojson', 'data': phase_conduits});
  parcel_source = map.addSource('parcel-data', {'type': 'geojson','data': parcels});
  delta_parcel_source = map.addSource('delta-parcel-data', {'type': 'geojson','data': delta_parcels});
  // node_source = map.addSource('node-data', {'type': 'geojson','data': nodes});

  // zoom_to_geojson(map, phase_conduits)

  map.addLayer({
      "id": "parcel",
      'type': 'fill',
      "source": "parcel-data",
      'paint': {
          'fill-color': {
              property: 'HoursFlooded',
              stops: [
                [0.0833, '#343332'],
                [2.0, '#f91313']
              ]
            },
          'fill-opacity': 0.8,
      },
      'layout': {
            'visibility': 'none'
        },
	}, 'wwgravmains-trunks');
  map.addLayer({
      "id": "delta-parcel",
      'type': 'fill',
      "source": "delta-parcel-data",
      'paint': {
          'fill-color': {
              property: 'DeltaHours',
              stops: [
                [-2.0, '#2AB200'],
                [-0.25, '#254C19'],
                [0.25, '#7F006D'],
                [2.0, '#B20098'],
              ]
            },
          'fill-opacity': 0.8,
      },
      'layout': {
            'visibility': 'none'
        },
	}, 'wwgravmains-trunks');

  $.each(nxt_phases, function(key, val){
    //add each next face conduits to the map
    data_source = key+'-data';
    map.addSource(data_source, {'type': 'geojson', 'data': val});
    map.addLayer({
        "id": key,'type': 'line',"source": data_source,
        'paint': {
            'line-color': '#64bab4',
            'line-opacity': 0.8,
    	      'line-width':4,
            'line-dasharray':[0.5,0.5],
        },
        'layout': {'visibility': 'none'},
  	});
  });

  $('tr.phase_hover').hover(function() {
    map.setLayoutProperty(this.dataset.phase, 'visibility', 'visible');},
    function (){
      map.setLayoutProperty(this.dataset.phase, 'visibility', 'none');
    }
  );
  map.addLayer({
      "id": "sewer",
      'type': 'line',
      "source": "sewer-data",
      'paint': {
          'line-color': '#4c4cbf',//'#64bab4',
          'line-opacity': 1,
  	      'line-width':4,
      },
      'layout': {
            'visibility': 'visible'
        },
	});
  map.addLayer({
        "id": "sewer-hover",
        'type': 'line',
        "source": "sewer-data",
        'paint': {
            'line-color': "#00bcd4",
            'line-opacity': 1,
			'line-width':4,
        },
		'filter':["==", "'InletNode'", ""],
    'layout': {
            'visibility': 'visible'
        },
  });
  map.addLayer({
      "id": "parcel-extrusion",
      'type': 'fill-extrusion',
      "source": "parcel-data",
      'paint': {
          'fill-extrusion-color': {
              property: 'HoursFlooded',
              stops: [
                [0.0833, '#343332'],
                [2.0, '#f91313']
              ]
            },
            'fill-extrusion-height': {
                property: 'HoursFlooded',
                stops: [
                  [0.0833, 0],
                  [2.0, 200]
                ]
            },
          'fill-extrusion-opacity': 0.85,
      },
      'layout': {
            'visibility': 'none'
        },
	});
  map.addLayer({
      "id": "delta-parcel-extrusion",
      'type': 'fill-extrusion',
      "source": "delta-parcel-data",
      'paint': {
          'fill-extrusion-color': {
              property: 'DeltaHours',
              stops: [
                [-2.0, '#2AB200'],
                [-0.25, '#254C19'],
                [0.25, '#7F006D'],
                [2.0, '#B20098'],
              ]
            },
            'fill-extrusion-height': {
                property: 'DeltaHours',
                stops: [
                  [-2.0, 200],
                  [-0.25, 5],
                  [0.25, 5],
                  [2.0, 200],
                ]
            },
          'fill-extrusion-opacity': 0.8,
      },
      'layout': {
            'visibility': 'none'
        },
	});


  map.addLayer({
      "id": "sheds",
      'type': 'line',
      'source': 'composite',
      "source-layer": "major_sewersheds-945jak",
      'paint': {
          'line-color':'rgb(125,139,202)',
          'line-width':1.0,
          'line-opacity':0.23
      },
      'layout': {
            'visibility': 'none'
        },
	}, 'parcel-extrusion');



    // When a click event occurs near a polygon, open a popup at the location of
    // the feature, with description HTML from its properties.
    map.on('click', function (e) {

		//create a buffer to forgive those clumsy clicks
		var x = e.point.x;
		var y = e.point.y;
		var clickbox = [[x-10, y-10], [x+10, y+10]]

    var features = map.queryRenderedFeatures(clickbox, { layers: ['sewer', 'wwgravmains-trunks',
                                                                  'wwgravmains-interceptors',
                                                                  'wwgravmains-branches'] });
    if (!features.length) {
	      map.setFilter("sewer-hover", ["==", "Name", ""]);
        return;
    }

    var feature = features[0];
    console.log(feature)

    if (feature.layer.id == 'sewer'){
      model_sewer_popup(map, feature, e)
    }
    if (feature.layer.id == "wwgravmains-trunks" ||
        feature.layer.id == "wwgravmains-interceptors" ||
        feature.layer.id == "wwgravmains-branches"){
        wwgrav_popup(map, feature, e)
    }


    });
    // Use the same approach as above to indicate that the symbols are clickable
    // by changing the cursor style to 'pointer'
    map.on('mousemove', function (e) {
        var features = map.queryRenderedFeatures(e.point, { layers: ['sewer', 'wwgravmains-trunks',
                                                                    'wwgravmains-interceptors',
                                                                    'wwgravmains-branches'] });
        map.getCanvas().style.cursor = (features.length) ? 'pointer' : '';
    });

    var toggleableLayerIds = ['sewer','parcel-extrusion', 'parcel',
                              'delta-parcel', 'delta-parcel-extrusion',
                              'wwgravmains-trunks',
                              'wwgravmains-interceptors',
                              'wwgravmains-branches', 'sheds'];

    for (var i = 0; i < toggleableLayerIds.length; i++) {
        var id = toggleableLayerIds[i];

        var anch = document.createElement('a')
        var link = document.createElement('li')
        link.appendChild(anch);
        link.href = '#';
        link.classList = 'primary';
        link.textContent = id;

        link.onclick = function (e) {
            var clickedLayer = this.textContent;
            e.preventDefault();
            e.stopPropagation();

            var visibility = map.getLayoutProperty(clickedLayer, 'visibility');

            if (visibility === 'visible') {
                map.setLayoutProperty(clickedLayer, 'visibility', 'none');
                this.classList.remove('primary');
                this.classList += ' default ';
            } else {
                this.classList.remove('default');
                this.classList += ' primary ';

                map.setLayoutProperty(clickedLayer, 'visibility', 'visible');
            }
        };

        var layers = document.getElementById('menu');
        layers.appendChild(link);
    };

    document.getElementById('POI-1').addEventListener('click', function() {
        map.flyTo({
            //Shunk and Philip Street
            center: [-75.151654, 39.915713],
            zoom: 18,
            bearing: 0,
        });
    });

});
