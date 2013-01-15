$(document).ready(function() {

	var $file_preview = $('@file-preview'),
		$file_info = $('@file-info');

	$file_preview.click(function() {
		$file_info.hide();
		$(this).hide('slide', {direction: 'left'}, 200, function() {
			$file_info.show('slide', {direction: 'right'}, 200);
		});
	});

	$('@file-preview-button').click(function() {
		$file_info.hide('slide', {direction: 'right'}, 200, function() {
			$file_preview.show('slide', {direction: 'left'}, 200);
		});
	});

});
