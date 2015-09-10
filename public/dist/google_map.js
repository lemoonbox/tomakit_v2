/**
 * Created by Mina on 2015-09-07.
 */
// This example displays an address form, using the autocomplete feature
// of the Google Places API to help users fill in the information.

var placeSearch, autocomplete;
var componentForm = {
    //street_number: 'short_name',
    street_address: 'short_name',
    //route: 'long_name',
    locality:'long_name',
    administrative_area_level_1: 'short_name',
    //country: 'long_name',
    sublocality_level_1: 'short_name',
    sublocality_level_2: 'short_name',
    sublocality_level_4: 'short_name',
    postal_code: 'short_name',
    premise: 'short_name'
};

function initAutocomplete() {
    // Create the autocomplete object, restricting the search to geographical
    // location types.
    autocomplete = new google.maps.places.Autocomplete(
        /** @type {!HTMLInputElement} */(document.getElementById('autocomplete')),
        {types: ['establishment', 'geocode']});

    // When the user selects an address from the dropdown, populate the address
    // fields in the form.
    autocomplete.addListener('place_changed', fillInAddress);
}

function fillInAddress() {
    // Get the place details from the autocomplete object.
    var place = autocomplete.getPlace();

    for (var component in componentForm) {
        document.getElementById(component).value = '';
        document.getElementById(component).disabled = false;

        //else if (document.getElementById(component).value = 0) {
        //    document.getElementById(component).addClass("hidden");
        //}
    }
    // Get each component of the address from the place details
    // and fill the corresponding field on the form.
    for (var i = 0; i < place.address_components.length; i++) {
        var addressType = place.address_components[i].types[0];
        if (componentForm[addressType]) {
            var val = place.address_components[i][componentForm[addressType]];
            document.getElementById(addressType).value = val;
            //if (val[i].length > 0) {
            //    document.getElementById(component).hidden = false;
            //}
            //else if (val[i].length =0) {
            //    document.getElementById(component).hidden = true;
            //}
            ////document.getElementById(component).hidden = document.getElementById(component).length == 0;
            //!(document.getElementById(component).length <= 0); {
            //    document.getElementById(component).Class("hidden");}
            //}
            //if (val !== 0) {
            //    document.getElementById(component).hidden = true;
            //}
        }
    }
}

// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var geolocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            var circle = new google.maps.Circle({
                center: geolocation,
                radius: position.coords.accuracy
            });
            autocomplete.setBounds(circle.getBounds());
        });
    }
}


//
//var data1 = {(document.getElementById(component)).value;
//if (data1.value.length > 0) {
//    data1.removeClass("hidden");
//}
//else if (data1().length = 0) {
//    data1.addClass("hidden");
//}

//if (component.value().length > 0) {
//    document.getElementById(component).removeClass("hidden");
//}
//else if (component.value().length = 0) {
//    document.getElementById(component).addClass("hidden");
//}