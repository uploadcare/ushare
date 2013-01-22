$(document).ready(function() {

	var slider = new Swipe($('#content').get(0));

	$('@file-info-button').click(function() {
		slider.next();
	});

	$('@file-preview-button').click(function() {
		slider.prev();
	});

});
