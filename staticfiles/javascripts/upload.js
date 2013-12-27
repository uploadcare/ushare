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
    };
})(jQuery);

$(function() {

    var clearSelections = function() {
        if (document.selection) {
            document.selection.empty();
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
        }
    };

    var progressTimeout, xhr;

    var uploadProgress = function(loaded) {
        // reserve 10% for local ajax thingies
        var reserved = 10;
        if (loaded > 1) {
            // sometimes uploadcare widget reports progress > 1
            loaded = 1;
        }
        $('@progress-bar .bar').width((loaded * 100 - reserved) + '%');
    };

    var uploadReset = function() {
        $('@progress-bar')
            .find('.progress')
            .removeClass('progress-success progress-danger')
            .addClass('progress-striped active')
            .find('.bar').width(0);
        clearTimeout(progressTimeout);

        if (xhr && xhr.abort != undefined) xhr.abort();
        $('@progress-bar, @upload-success, @upload-fail').addClass('hidden');
        $('@file-url-link').attr('href', '#');
        $('@file-url').val('');
        $('@file-url-path, @file-url-name').empty();
        $('@upload-form').removeClass('hidden');
        if (window.clip) window.clip.hide();
        clearSelections();
        widget.value('');
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

    var widget = uploadcare.Widget('@uploadcare-uploader');
    var currentFile;
    widget.onChange(function(file) {
        if (file) {
            currentFile = file;
            $('@upload-form').addClass('hidden');
            $('@progress-bar').removeClass('hidden');
            file.progress(function(uploadInfo) {
                if (file != currentFile) {
                    return;
                }
                uploadProgress(uploadInfo.progress);
            });
            file.fail(uploadReset);
            file.done(function() {
                if (file != currentFile) {
                    return;
                }
                // submit form. sends ajax request to ushare
                $('@upload-form').submit();
            });
        }
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

    $('@upload-form').submit(function(e) {
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
            success: function(data, status, jqXHR) {
                var url = jqXHR.getResponseHeader('Location');
                uploadComplete(url, data.file_obj);
            }
        });
    });

    $('@file-url-input')
        .mouseup(function(e) {
            e.preventDefault();
        }) 
        .focus(function() {
            $(this).selectNodeContents('focus');
        })
        .blur(function() {
            $(this).removeClass('focus');
        });

});
