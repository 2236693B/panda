$(document).ready( function() {
    $("p").hover( function() {
        $(this).css('color', 'red');
    },
    function() {
        $(this).css('color', 'black');
    });

    $("#about-btn").click( function(event) {
        alert("You clicked the button using JQuery!");
    });

});




