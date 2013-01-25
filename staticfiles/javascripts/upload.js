(function($) {
	$.fn.selectNodeContents = function(class_name) {
		var ieSelector = function(elem) {
			var range = document.body.createTextRange();
			range.moveToElementText(elem);
			range.select();
		},
		commonSelector = function(elem) {
			var selection = window.getSelection(),
				range = document.createRange();
			range.selectNodeContents(elem);
			selection.removeAllRanges();
			selection.addRange(range);
			},
		selectFunction = document.body.createTextRange ? ieSelector : commonSelector;

		$(this).each(function(index, elem) {
			selectFunction(elem);
			$(elem).addClass(class_name);
		});

			//window.getSelection
			// document.body.createTextRange
	};
})(jQuery);


$(document).ready(function() {

	var clearSelections = function() {
		if (document.body.createTextRange) {
			// TODO: Add IE-case here.
		}
		else {
			window.getSelection().removeAllRanges();
		};
	};

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

	var progressTimeout, xhr;

	var uploadProgress = function(loaded, total, reserved) {
		reserved = reserved || 0;
		var width = loaded / total
		$('@progress-bar .bar').width(((loaded / total) * 100 - reserved) + '%');
	};

	var uploadReset = function() {
		$('@progress-bar')
		.find('.progress').removeClass('progress-success progress-danger').addClass('progress-striped active')
			.find('.bar').width(0);
		clearTimeout(progressTimeout);
		if (xhr.abort != undefined) xhr.abort();
		$('@progress-bar, @upload-success, @upload-fail').addClass('hidden');
		$('@file-url-link').attr('href', '#');
		$('@file-url').val('');
		$('@file-url-path, @file-url-name').empty();
		$('@upload-form').removeClass('hidden');
		if (window.clip) window.clip.hide();
		clearSelections();
	};

	var uploadComplete = function(file_url, errors) {
		var result_class = file_url ? 'progress-success' : 'progress-danger',
			error_message = errors ? errors[0] : 'Error',
			$progress_bar = $('@progress-bar');

		$('.bar', $progress_bar).width(100 + '%');

		progressTimeout = setTimeout(function() {
			$('.progress', $progress_bar).removeClass('progress-striped active').addClass(result_class);
			progressTimeout = setTimeout(function() {
				$progress_bar.addClass('hidden');
				if (file_url) {
					var last_slash_index = file_url.lastIndexOf('/'),
						short_url = file_url.substring(0, last_slash_index + 1),
						filename = file_url.substring(last_slash_index + 1);

					$('@upload-success').removeClass('hidden')
						.find('@file-url').val(file_url).end()
						.find('@file-url-path').html(short_url).end()
						.find('@file-url-name').html(filename).end()
						.find('@file-url-link').attr('href', file_url);
					initClipBoard();
				}
				else {
					$('@upload-fail').removeClass('hidden').find('@error-message').html(error_message);
				};
			}, 300);
		}, 500);
	};

	var widget = $('@uploadcare-uploader').data('widget');

	$([widget.upload.uploaders.file, widget.upload.uploaders.url])
		.on('uploadcare.api.uploader.start', function(e) {
			$('@upload-form').addClass('hidden');
			$('@progress-bar').removeClass('hidden');
		})
		.on('uploadcare.api.uploader.progress', function(e){
			uploadProgress(e.target.loaded, e.target.fileSize, 10);
		})
		.on('uploadcare.api.uploader.error', function() {
			uploadReset();
		});

	$('@upload-cancel-button').click(function() {
		$(widget.template).trigger('uploadcare.widget.template.cancel');
		uploadReset();
	});

	$('@upload-reset').click(function(e) {
		e.preventDefault();
		$(widget.template).trigger('uploadcare.widget.template.remove');
		uploadReset();
	});

	$('@upload-form').submit(function(e){
		e.preventDefault();
		var $this = $(this);
		xhr = $.ajax({
			data: $this.serialize(),
			url: $this.attr('action'),
			type: $this.attr('method'),
			context: $this,
			error: function(request, status) {
				if (status != 'abort') uploadComplete(false, ['Error',]);
			},
			success: function(data) {
				uploadComplete(data.url, data.file_obj)
			}
		});
	});

	$('@file-url-input:not(.focus)').click(function() {
		$(this).selectNodeContents('focus');
	});

	$('body').click(function(e) {
		$('@file-url-input').not(e.target).removeClass('focus');
	});

	$('@uploadcare-uploader').change(function() {
		if ($(this).val()) {
			$(this).closest('form').submit();
		};
	});

});
