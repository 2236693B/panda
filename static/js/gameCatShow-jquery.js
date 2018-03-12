$(document).ready( function() {
	$('div.catergory').on('click', 'toggleButton', function(e){
		alert("Please log in");

		cat = $(e.delegateTarget).find('catGames');
		cat.is(':hidden') ? cat.show() : cat.hide();
	});
});
