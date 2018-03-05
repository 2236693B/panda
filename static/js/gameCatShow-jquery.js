$(document).ready( function() {
    $('toggleGames').click(function() {
        if ($('catGames').is(':visible')) {
            $('catGames').hide();
        } else {
            $('catGames').show();
        }
    });
});
