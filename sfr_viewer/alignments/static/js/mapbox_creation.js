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

var map_layers = {
  parcel_risk:{
    'id':'parcel',
    'source':'parcel-data',
    'paint': {
      'fill-color': {property: 'HoursFlooded',stops: [[0.0833, '#343332'],[2.0, '#f91313']]},
      'fill-opacity': 0.8,
    },
    'layout': {'visibility': 'none'},
    'name':'Risk (parcel-hours)',
    'type': 'fill',
  },
  parcel_benefit:{
    'id':'delta-parcel',
    'source':'delta-parcel-data',
    'paint': {
      'fill-color': {
        property: 'DeltaHours',
        stops:[
          [-2.0, '#2AB200'],
          [-0.25, '#254C19'],
          [0.25, '#7F006D'],
          [2.0, '#B20098'],
        ]
      },
      'fill-opacity': 0.8,
    },
    'layout': {'visibility': 'none'},
    'name':'Risk Reduction (parcel-hours)',
    'type': 'fill',
  },
  proposed_sewers:{
    name:'Proposed Sewers',
    id: "sewer",
    'type': 'line',
    "source": "sewer-data",
    'paint': {
      'line-color': '#4c4cbf',
      'line-opacity': 1,
      'line-width':4,
    },
    'layout': {'visibility': 'visible'},
	},
  proposed_sewers_hover:{
    id: "sewer-hover",
    type: 'line',
    source: "sewer-data",
    paint: {
        'line-color': "#00bcd4",
        'line-opacity': 1,
	      'line-width':4,
    },
		filter:["==", "'InletNode'", ""],
    layout: {'visibility': 'visible'},
  },
  parcel_3d:{
      name:'Risk (3D)',
      id: "parcel-extrusion",
      type: 'fill-extrusion',
      source: "parcel-data",
      'paint': {
        'fill-extrusion-color': {
          property: 'HoursFlooded',
          stops: [[0.0833, '#343332'],[2.0, '#f91313']]
        },
        'fill-extrusion-height': {
          property: 'HoursFlooded',
          stops: [[0.0833, 0],[2.0, 200]]
        },
        'fill-extrusion-opacity': 0.85,
      },
      'layout': {'visibility': 'none'},
	},
  benefit_3d:{
    name:'Risk Reduction (3D)',
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
    'layout': {'visibility': 'none'},
	},
  sheds:{
    name:'Sewer Sheds',
      "id": "sheds",
      'type': 'line',
      'source': 'composite',
      "source-layer": "major_sewersheds-945jak",
      'paint': {
        'line-color':'rgb(125,139,202)',
        'line-width':1.0,
        'line-opacity':0.23
      },
      'layout': {'visibility': 'none'},
	},
  trunks:{
    name:'Trunks',
    id:'wwgravmains-trunks',
    'layout': {'visibility': 'visible'},
  },
  interceptors:{
    name:'Interceptors',
    id:'wwgravmains-interceptors'
  },
  branches:{
    name:'Branches',
    id:'wwgravmains-branches'
  }


}

map.on('load', function() {

  //load the data into the map
  sewer_source = map.addSource('sewer-data', {'type': 'geojson', 'data': phase_conduits});
  parcel_source = map.addSource('parcel-data', {'type': 'geojson','data': parcels});
  delta_parcel_source = map.addSource('delta-parcel-data', {'type': 'geojson','data': delta_parcels});

  map.addLayer(map_layers.parcel_risk, 'wwgravmains-trunks');
  map.addLayer(map_layers.parcel_benefit, 'wwgravmains-trunks');

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
  // map.addLayer(map_layers.trunks);
  map.addLayer(map_layers.proposed_sewers);
  map.addLayer(map_layers.proposed_sewers_hover);
  map.addLayer(map_layers.parcel_3d);
  map.addLayer(map_layers.benefit_3d);
  map.addLayer(map_layers.sheds, 'parcel-extrusion');



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

    var toggleableLayers = ['proposed_sewers','trunks','interceptors',
                            'branches', '-divider-', 'parcel_3d', 'parcel_risk',
                            'parcel_benefit', 'benefit_3d','-divider-','sheds'];


    for (var i = 0; i < toggleableLayers.length; i++) {

        //build the layer toggle menu
        var layers_menu = document.getElementById('menu');
        var layer = toggleableLayers[i];

        if (layer =='-divider-'){
          var divider = document.createElement('li')
          divider.role = 'separator';
          divider.classList = 'divider';
          layers_menu.appendChild(divider);
          continue;
        }

        var id = map_layers[layer].id
        var anch = document.createElement('a')
        anch.textContent = map_layers[layer].name;

        anch.href = '#';
        anch.classList = 'primary';

        var link = document.createElement('li')
        link.appendChild(anch);
        link.dataset.layer_id = id;

        //assign the default visibility setting
        if (map.getLayoutProperty(id, 'visibility') === 'visible'){
          link.classList += ' active ';
        }else{
          link.classList.remove('active');
        }

        link.onclick = function (e) {
            var clickedLayer = this.textContent;
            var layerid = this.dataset.layer_id;
            console.log(this)
            e.preventDefault();
            e.stopPropagation();

            var visibility = map.getLayoutProperty(layerid, 'visibility');

            if (visibility === 'visible') {
                map.setLayoutProperty(layerid, 'visibility', 'none');
                this.classList.remove('active');
                // this.classList += ' default ';
            } else {
                this.classList += ' active ';
                // this.classList += ' active ';

                map.setLayoutProperty(layerid, 'visibility', 'visible');
            }
        };

        // var layers = document.getElementById('menu');
        layers_menu.appendChild(link);
    };

});
