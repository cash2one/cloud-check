function loadingImg() {
    var colors = ['black']
    var square = new Sonic({

        width: 100,
        height: 100,

        stepsPerFrame: 3,
        trailLength: 1,
        pointDistance: .01,
        fps: 30,
        step: 'fader',

        strokeColor: '#EEA236',

        setup: function() {
            this._.lineWidth = 8;
        },

        path: [
            ['arc', 50, 50, 20, 360, 0]
        ]
    });
    square.play();
    $("#loading_canvas").html(square.canvas);
}

function show_loading(){
    $("#pjax-container").css("opacity", "0.8");
    $('#loading_canvas').show();
    send_init_message();
}

function hide_loading(){
    $("#pjax-container").css("opacity", "1");
    $('#loading_canvas').hide();
}

$(function(){
    loadingImg();
    $(document).pjax('a[data-pjax]', '#pjax-container', {fx: 'fade', timeout: 9000});
    // $(document).pjax('a[data-pjax]', '#pjax-container',
    //     {
    //         fx: 'fade',
    //         timeout: 9000
    //     }
    // );
    
    $(document).on('submit', 'form[data-pjax]', function(event) {
        $.pjax.submit(event, '#pjax-container', {fx: 'fade', timeout: 9000});
    });
    $.pjax.defaults.timeout = 9000;

    $(document).on('pjax:start', function(xhr, options) {
        console.log('start');
        show_loading()
        // $("#pjax-container").css("opacity", "0.8");
        // $('#loading_canvas').show();
    });
    $(document).on('pjax:end', function(xhr, options) {
        // console.log(options);
        var title = decodeURI(options.getResponseHeader('title'));
        var origin_title = $(document).find('title').text();
        var first = origin_title.split(" - ")[0];
        $(document).find('title').text(first + ' - ' + title);
        var active = decodeURI(options.getResponseHeader('active'));
        $(document).find('ul.sidebar-menu').find('li').removeClass('active');
        $(document).find('ul.sidebar-menu').find('a[name="'+active+'"]').parent().addClass('active');

        console.log('end');
        hide_loading();
        // $("#pjax-container").css("opacity", "1");
        // $('#loading_canvas').hide();
    });
    $(document).on('pjax:complete', function() {
        // alert('complete ... ');
    });

    try{
      $(".fa-refresh").parent().attr("href", window.location.href)
    }catch(e){}
})

