/**
 * Created by Mina on 2015-09-07.
 */
// This example displays an address form, using the autocomplete feature
// of the Google Places API to help users fill in the information.

//var placeSearch, autocomplete;
var componentForm = {
    street_address: 'short_name',
    locality:'long_name',
    administrative_area_level_1: 'short_name',
    sublocality_level_1: 'short_name',
    sublocality_level_2: 'short_name',
    sublocality_level_4: 'short_name',
    postal_code: 'short_name',
    premise: 'short_name'
};

//function initAutocomplete() {
//    // Create the autocomplete object, restricting the search to geographical
//    // location types.
//    autocomplete = new google.maps.places.Autocomplete(
//        /** @type {!HTMLInputElement} */(document.getElementById('pac-input')),
//        {types: ['geocode', 'establishment']});
//
//    // When the user selects an address from the dropdown, populate the address
//    // fields in the form.
//    autocomplete.addListener('place_changed', fillInAddress);
//}
//

//// Bias the autocomplete object to the user's geographical location,
//// as supplied by the browser's 'navigator.geolocation' object.
//function geolocate() {
//    if (navigator.geolocation) {
//        navigator.geolocation.getCurrentPosition(function(position) {
//            var geolocation = {
//                lat: position.coords.latitude,
//                lng: position.coords.longitude
//            };
//            var circle = new google.maps.Circle({
//                center: geolocation,
//                radius: position.coords.accuracy
//            });
//            autocomplete.setBounds(circle.getBounds());
//        });
//    }
//}
//

function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.563311, lng: 126.978262},
        zoom: 13
    });
    google.maps.event.addListenerOnce(map, 'idle', function(){
        // do something only the first time the map is loaded

    });
    //google.maps.event.addDomListener(window, 'load', initMap);
    var input = /** @type {!HTMLInputElement} */(
        document.getElementById('pac-input'));

    var types = document.getElementById('type-selector');
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(types);

    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo('bounds', map);

    // Create the autocomplete object, restricting the search to geographical
    // location types.
    autocomplete = new google.maps.places.Autocomplete(
        /** @type {!HTMLInputElement} */(document.getElementById('pac-input')),
        {types: ['geocode', 'establishment']});

    // When the user selects an address from the dropdown, populate the address
    // fields in the form.
    autocomplete.addListener('place_changed', fillInAddress);


    var infowindow = new google.maps.InfoWindow();
    var marker = new google.maps.Marker({
        map: map,
        anchorPoint: new google.maps.Point(0, -29)
    });

    autocomplete.addListener('place_changed', function() {
        infowindow.close();
        marker.setVisible(false);
        var place = autocomplete.getPlace();
        if (!place.geometry) {
            window.alert("Autocomplete's returned place contains no geometry");
            return;
        }

        // If the place has a geometry, then present it on a map.
        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);  // Why 17? Because it looks good.
        }
        marker.setIcon(/** @type {google.maps.Icon} */({
            url: place.icon,
            size: new google.maps.Size(71, 71),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(17, 34),
            scaledSize: new google.maps.Size(35, 35)
        }));
        marker.setPosition(place.geometry.location);
        marker.setVisible(true);

        var address = '';
        if (place.address_components) {
            address = [
                (place.address_components[0] && place.address_components[0].short_name || ''),
                (place.address_components[1] && place.address_components[1].short_name || ''),
                (place.address_components[2] && place.address_components[2].short_name || '')
            ].join(' ');
        }

        infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
        infowindow.open(map, marker);
    });



    function fillInAddress() {
        // Get the place details from the autocomplete object.
        var place = autocomplete.getPlace();

        for (var component in componentForm) {
            document.getElementById(component).value = '';
            document.getElementById(component).disabled = false;
        }
        // Get each component of the address from the place details
        // and fill the corresponding field on the form.
        for (var i = 0; i < place.address_components.length; i++) {
            var addressType = place.address_components[i].types[0];
            if (componentForm[addressType]) {
                var val = place.address_components[i][componentForm[addressType]];
                document.getElementById(addressType).value = val;
            }
        }
    }


    // Sets a listener on a radio button to change the filter type on Places
    // Autocomplete.
    function setupClickListener(id, types) {
        var radioButton = document.getElementById(id);
        radioButton.addEventListener('click', function() {
            autocomplete.setTypes(types);
        });
    }

    setupClickListener('changetype-all', []);
    setupClickListener('changetype-address', ['address']);
    setupClickListener('changetype-establishment', ['establishment']);
    setupClickListener('changetype-geocode', ['geocode']);
}