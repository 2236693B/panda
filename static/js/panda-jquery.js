//Make links change colour on hover

$(document).ready( function() {

    $("highlight").hover( function() {
        $(this).css('color', 'red');
        $(this).css('font-weight', 'bold');

    },
    function() {
        $(this).css('color', 'white');
        $(this).css('font-weight', 'normal');

    });

//Generate warning when player not logged in
    $("NL").click( function() {
        alert("Please log in");
    });

});




