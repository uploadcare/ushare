$(document).ready(function(){
	var drawFieldErrors = function(field_name, field_errors) {
		var $field = $('[name=' + field_name + ']'),
			$field_wrapper = $field.parent('div.field-wrapper'),
			$error_list = $field_wrapper.children('ul.field-error-list'),
			$empty_error = $error_list.children('li.empty-elem');

		$.each(field_errors, function() {
			$empty_error.clone().removeClass('empty-elem').html(this.toString()).appendTo($error_list);
		});
		$field_wrapper.addClass('error');
	};

	var clearFieldErrors = function(container) {
		var $container = $(container || 'body');
		$container
			.find('ul.field-error-list li:not(.empty-elem)').remove().end()
			.find('.error').removeClass('error');
	};

	$('#id_upload-form').submit(function(e){
		e.preventDefault();
		$(this).ajaxSubmit({
			context: this,
			beforeSend: function() {
				$(this).find(':submit').attr('disabled', true).end()
				clearFieldErrors(this);
			},
			complete: function() {
				$(':submit', this).attr('disabled', false);
			},
			success: function(data) {
				var file_url = data.url;
				if (file_url) {
					$(':submit', this).hide();
					$('input.file-url').val(file_url);
					$('.upload-success.hidden').removeClass('hidden');
				}
				else {
					$.each(data, drawFieldErrors);
				};
			}
		});
	});

	$('input.file-url').click(function() {
		$(this).select();
	});
});
