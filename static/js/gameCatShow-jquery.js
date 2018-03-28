//Display clicked category name

$(document).ready( function() {
	$('div.catergory').on('click', 'toggleButton', function(e){
		cat = $(e.delegateTarget).find('catGames');
		if (cat.is(':hidden')){
			cat.show()
		} 
		else{
			cat.hide()
		}
	});
});
