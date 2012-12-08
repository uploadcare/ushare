$(document).ready(function() {

	var initClipBoard = function() {
		if (!window.clip) {
			window.clip = new ZeroClipboard.Client();
			clip.setHandCursor(true);
			clip.glue($('@clipboard-copy-button').get(0));

			clip.addEventListener('onMouseDown', function(client) {
				clip.setText($('@file-url').val());
			});
		}
		else {
			window.clip.show();
		};
	};

	var uploadProgress = function(loaded, total, reserved) {
		reserved = reserved || 0;
		var width = loaded / total
		$('@progress-bar .bar').width(((loaded / total) * 100 - reserved) + '%');
	};

	var uploadReset = function() {
		$('@progress-bar')
		.find('.progress').removeClass('progress-success progress-danger').addClass('progress-striped active')
			.find('.bar').width(0);
		$('@progress-bar, @upload-success, @upload-fail').addClass('hidden');
		$('@upload-form').removeClass('hidden');
		if (window.clip) window.clip.hide();
	};

	var uploadComplete = function(file_url, errors) {
		var result_class = file_url ? 'progress-success' : 'progress-danger',
			error_message = errors ? errors[0] : 'Error',
			$progress_bar = $('@progress-bar');

		$('.bar', $progress_bar).width(100 + '%');

		setTimeout(function() {
			$('.progress', $progress_bar).removeClass('progress-striped active').addClass(result_class);
			setTimeout(function() {
				$progress_bar.addClass('hidden');
				if (file_url) {
					$('@upload-success').removeClass('hidden').find('@file-url').val(file_url);
					initClipBoard();
				}
				else {
					$('@upload-fail').removeClass('hidden').find('@error-message').html(error_message);
				};
				}, 300);
			}, 500);
	};

	var widget = $('@uploadcare-uploader').data('widget');

	$(widget.uploaders.file)
		.on('uploadcare.api.uploader.start', function(e) {
			$('@upload-form').addClass('hidden');
			$('@progress-bar').removeClass('hidden');
		})
		.on('uploadcare.api.uploader.progress', function(e){
			uploadProgress(e.target.loaded, e.target.fileSize, 10);
		});

	$('@upload-cancel-button').click(function() {
		$(widget.template).trigger('uploadcare.widget.template.cancel');
		uploadReset()
	});

	$('@upload-reset').click(function(e) {
		e.preventDefault();
		$(widget.template).trigger('uploadcare.widget.template.remove');
		uploadReset();
	});

	$('@upload-form').submit(function(e){
		e.preventDefault();
		$(this).ajaxSubmit({
			context: this,
			error: function() {
				uploadComplete(false, ['Error',]);
			},
			success: function(data) {
				uploadComplete(data.url, data.file_obj)
			}
		});
	});

	$('@file-url').click(function() {
		$(this).select();
	});

	$('@uploadcare-uploader').change(function() {
		if ($(this).val()) {
			$(this).closest('form').submit();
		};
	});

});
