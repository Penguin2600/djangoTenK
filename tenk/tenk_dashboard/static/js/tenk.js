function getZip(zipCode) {
    var zip = zipCode;
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({
        'address' : zip
    }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            if (results[0]) {
                console.log(results[0])
                city = results[0].formatted_address.split(',')[0].toUpperCase();
                state = results[0].formatted_address.split(',')[1].split(" ")[1].toUpperCase();
                $('#id_city').val(city);
                $('#id_state').val(state);
            }
        }
    });
}

//validate bib not in use
jQuery.validator.addMethod("bibnumber", function(value) {
    var isSuccess = false;

    $.ajax({
        url : '/checkbib/'+value,
        async : false,
        data : {},
        success : function(output) {
            isSuccess = output === "false" ? true : false;
        }
    });

    return isSuccess;

}, "Bib In Use");

jQuery.validator.addMethod("zipcode", function(value, element) {
    return this.optional(element) ||  /\d{5}-\d{4}$|^\d{5}$|^[a-zA-Z][0-9][a-zA-Z](| )?[0-9][a-zA-Z][0-9]$/.test(value);
}, "The specified US ZIP Code is invalid");


jQuery.validator.addMethod("search_results", function(value) {
    var isSuccess = false;

    $.ajax({
        url : '/checksearch/'+value,
        async : false,
        data : {},
        success : function(output) {
            isSuccess = output === "false" ? true : false;
        }
    });

    return isSuccess;

}, "No Results");

$(document).ready(function() {

    $("#id_bib_number").focus();

    $('#id_zipcode').live('blur', function() {
        getZip($('#id_zipcode').val());
    });

    $("#createform").validate({
        onkeyup : false,
        onclick : false,
        rules : {
            bib_number : {
                required : true,
                digits : true,
                bibnumber : true
            },
            first_name : "required",
            last_name : "required",
            zipcode : {
                zipcode: true,
            },
            age : {
                required : true,
                range : [1, 99],
                digits : true
            },

            email : {
                email : true
            },

            shirt_size : "required",
            gender : "required",
            registration_type : "required",
            event : "required",
            division : "required"
        },
        submitHandler : function(form) {
            form.submit();
        }
    });

    $("#updateform").validate({
        onkeyup : false,
        onclick : false,
        rules : {
            bib_number : {
                required : true,
                digits : true
            },
            first_name : "required",
            last_name : "required",
            zipcode : {
                zipcode: true,
            },
            age : {
                required : true,
                range : [1, 99],
                digits : true
            },

            email : {
                email : true
            },

            shirt_size : "required",
            gender : "required",
            registration_type : "required",
            event : "required",
            division : "required"
        },
        submitHandler : function(form) {
            form.submit();
        }
    });
});

