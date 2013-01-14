$(document).ready(function() {

	$('@file-info-button').click(function() {
		$('@file-info').hide();
		$('@file-image').hide('slide', {direction: 'left'}, 200, function() {
			$('@file-info').show('slide', {direction: 'right'}, 200);
		});
	});

	$('@file-image-button').click(function() {
		$('@file-info').hide('slide', {direction: 'right'}, 200, function() {
			$('@file-image').show('slide', {direction: 'left'}, 200);
		});
	});

});
