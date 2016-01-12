$(document).ready(function() {
    // pjax
    $(document).pjax('[data-pjax] a, a[data-pjax]', '#pjax', {
        timeout: 1000
    })

    $(document).on('pjax:click', function(options) {
        console.log('click');
    });
    $(document).on('pjax:clicked', function(options) {
        console.log('clicked');
    });
    $(document).on('pjax:start', function(xhr, options) {
        console.log('start');
        $('#container').dimmer('show');
    });
    $(document).on('pjax:end', function(xhr, options) {
        console.log('end');
        setTimeout(function() {
            $('#container').dimmer('hide');
        }, 600);
    });
    $(document).on('pjax:success', function(data, status, xhr, options) {
        console.log('success');
    });

    $(document).on('pjax:timeout', function(xhr, options) {
        console.log('timeout');
    });
    $(document).on('pjax:error', function(xhr, textStatus, error, options) {
        console.log('error');
    });
    $(document).on('pjax:complete', function(xhr, textStatus, options) {
        console.log('complete');

    });
    $(document).on('pjax:beforeReplace', function(contents, options) {
        console.log('beforeReplace');
    });
    $(document).on('pjax:beforeSend', function(xhr, options) {
        console.log('beforeSend');
    });


    // semantic api

    // $.fn.api.settings.api = {
    //     "user_signin": "/api/account/signin",
    //     "image_edit": "/admin/image/edit/{pk}"
    // }

    // $.fn.api.settings.errorDuration = 6000;
    // $.fn.api.settings.method = 'post';
    // $.fn.api.settings.serializeForm = true;
    // $.fn.api.settings.beforeXHR = function(xhrObject) {
    //     // console.log(xhrObject);
    // }

    // $.fn.api.settings.onFailure = function(response, element) {
    //     $('#notification').notify({
    //         category: response.category,
    //         title: response.title || '',
    //         content: response.message
    //     })
    // }
    // $.fn.api.settings.successTest = function(response) {
    //     return response.success || false;
    // }
    // $.fn.api.settings.onSuccess = function(response, element, xhr) {
    //     $('#notification').notify({
    //         category: response.category,
    //         title: response.title || '',
    //         content: response.message
    //     })
    // }
    // $.fn.api.settings.onError = function(errorMessage, element, xhr) {
    //     $('#notification').notify({
    //         category: 'red',
    //         title: 'error',
    //         content: errorMessage
    //     })
    // }
    // $.fn.api.settings.onAbort = function(errorMessage, element, xhr) {
    //     $('#notification').notify({
    //         category: 'red',
    //         title: 'error',
    //         content: errorMessage
    //     })
    // }
    // $.fn.api.settings.onComplete = function(response, element, xhr) {
    //     console.log('onComplete');
    // }

    $('body').on('click', '.message .close', function(e) {
        $(this).closest('.message').transition('fade');
    });
});

// plugins

(function($) {
    $.fn.extend({
        notify: function(options) {

            var defaults = {
                container: '#container',
                category: 'success',
                title: '',
                content: 'ok'
            };

            var options = $.extend(defaults, options);

            if (this) {
                this.remove();
            }

            var html = '<div id="notification" class="ui floating message {{ category }}">' +
                '<i class="close icon"></i>' +
                '<div class="header">{{ title }}</div>' +
                '<p>{{ content }}</p></div>';
            var template = Handlebars.compile(html);
            $(template({
                category: options.category,
                title: options.title,
                content: options.content
            })).prependTo($(options.container));

            return this;
        }
    });
})(jQuery);
