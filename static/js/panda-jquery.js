$(document).ready( function() {

    $("highlight").hover( function() {
        $(this).css('color', 'red');
        $(this).css('font-weight', 'bold');

    },
    function() {
        $(this).css('color', 'black');
        $(this).css('font-weight', 'normal');

    });

    $("NL").click( function() {
        alert("Please log in to view profiles");
    });

});




