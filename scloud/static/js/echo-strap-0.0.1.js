/**
 * ***************************************************************************************************
 * echo-strap 0.0.1
 * based on Jquery & Bootstrap
 * author: zhangpeng <zhangpeng820213@gmail.com>
 * date:2013-12-18
 * ***************************************************************************************************
 */


(function ($) { 

/**
 * ***************************************************************************************************
 * 扩展JQuery函数 (jquery extend functions)
 * ***************************************************************************************************
 */

$.extend(String.prototype, {
  /**
   * 字符串格式化
   * 'test{0}{1}'.format(var1,var2);
   */
  format: function(){
    var args = arguments;
    var str = this;
    for(var i=0; i<args.length; i++){
      var re = new RegExp('\\{' + i + '\\}','gm');
      str = str.replace(re, args[i]);
    }
    return str
  },
  parseQueryString: function(){
    var str=this;
    var items=str.split("&");
    var result={}
    var arr=null;
    for(var i=0; i<items.length; i++){
      var reg = new RegExp(/(\w+)?(=)?(\S+)?/gi)
      arr = reg.exec(items[i])
      if (!$defined(arr[1])){
          result[""] = arr[3];
      }else if(!$defined(arr[2])){
          //result[""] = arr[0];
      }else if (!$defined(arr[3])){
          result[arr[1]] = "";
      }else{
        result[arr[1]]=arr[3];
      }
    }
    return result;
  }
})

$.fn['toggles'] = function(options) {
  options = options || {};

  // extend default opts with the users options
  var opts = $.extend({
    'drag': true, // can the toggle be dragged
    'click': true, // can it be clicked to toggle
    'text': {
      'on': 'ON', // text for the ON position
      'off': 'OFF' // and off
    },
    'on': false, // is the toggle ON on init
    'animate': 250, // animation time
    'transition': 'ease-in-out', // animation transition,
    'checkbox': null, // the checkbox to toggle (for use in forms)
    'clicker': null, // element that can be clicked on to toggle. removes binding from the toggle itself (use nesting)
    'width': 50, // width used if not set in css
    'height': 20, // height if not set in css
    'type': 'compact' // defaults to a compact toggle, other option is 'select' where both options are shown at once
  },options);

  var selectType = (opts['type'] == 'select');

  // ensure these are jquery elements
  opts['checkbox'] = $(opts['checkbox']); // doesnt matter for checkbox

  if (opts['clicker']) opts['clicker'] = $(opts['clicker']); // leave as null if not set

  // use native transitions if possible
  var transition = 'margin-left '+opts['animate']+'ms '+opts['transition'];
  var transitions = {
    '-webkit-transition': transition,
    '-moz-transition': transition,
    'transition': transition
  };

  // for resetting transitions to none
  var notransitions = {
    '-webkit-transition': '',
    '-moz-transition': '',
    'transition': ''
  };

  // this is the actual toggle function which does the toggling
  var doToggle = function(slide, width, height, state) {
    var active = slide.toggleClass('active').hasClass('active');

    if (state === active) return;

    var inner = slide.find('.toggle-inner').css(transitions);

    slide.find('.toggle-off').toggleClass('active');
    slide.find('.toggle-on').toggleClass('active');

    // toggle the checkbox, if there is one
    opts['checkbox'].prop('checked',active);

    if (selectType) return;

    var margin = active ? 0 : -width + height;

    // move the toggle!
    inner.css('margin-left',margin);

    // ensure the toggle is left in the correct state after animation
    setTimeout(function() {
      inner.css(notransitions);
      inner.css('margin-left',margin);
    },opts['animate']);

  };

  // start setting up the toggle(s)
  return this.each(function() {
    var toggle = $(this);

    var height = toggle.height();
    var width = toggle.width();

    // if the element doesnt have an explicit height/width in css, set them
    if (!height || !width) {
      toggle.height(height = opts.height);
      toggle.width(width = opts.width);
    }

    var div = '<div class="toggle-';
    var slide = $(div+'slide">'); // wrapper inside toggle
    var inner = $(div+'inner">'); // inside slide, this bit moves
    var on = $(div+'on">'); // the on div
    var off = $(div+'off">'); // off div
    var blob = $(div+'blob">'); // the grip toggle blob

    var halfheight = height/2;
    var onoffwidth = width - halfheight;

    // set up the CSS for the individual elements
    on
      .css({
        height: height,
        width: onoffwidth,
        textAlign: 'center',
        textIndent: selectType ? '' : -halfheight,
        lineHeight: height+'px'
      })
      .html(opts['text']['on']);

    off
      .css({
        height: height,
        width: onoffwidth,
        marginLeft: selectType ? '' : -halfheight,
        textAlign: 'center',
        textIndent: selectType ? '' : halfheight,
        lineHeight: height+'px'
      })
      .html(opts['text']['off'])
      .addClass('active');

    blob.css({
      height: height,
      width: height,
      marginLeft: -halfheight
    });

    inner.css({
      width: width * 2 - height,
      marginLeft: selectType ? 0 : -width + height
    });

    if (selectType) {
      slide.addClass('toggle-select');
      toggle.css('width', onoffwidth*2);
      blob.hide();
    }

    // construct the toggle
    toggle.html(slide.html(inner.append(on,blob,off)));

    // when toggle is fired, toggle the toggle
    slide.on('toggle', function(e,active) {

      // stop bubbling
      if (e) e.stopPropagation();

      doToggle(slide,width,height);
      toggle.trigger('toggle',!active);
    });

    // setup events for toggling on or off
    toggle.on('toggleOn', function() {
      doToggle(slide, width, height, false);
    });
    toggle.on('toggleOff', function() {
      doToggle(slide, width, height, true);
    });

    if (opts['on']) {

      // toggle immediately to turn the toggle on
      doToggle(slide,width,height);
    }

    // if click is enabled and toggle isn't within the clicker element (stops double binding)
    if (opts['click'] && (!opts['clicker'] || !opts['clicker'].has(toggle).length)) {

      // bind the click, ensuring its not the blob being clicked on
      toggle.on('click touchstart',function(e) {
        e.stopPropagation();

        if (e.target !=  blob[0] || !opts['drag']) {
          slide.trigger('toggle', slide.hasClass('active'));
        }
      });
    }

    // setup the clicker element
    if (opts['clicker']) {
      opts['clicker'].on('click touchstart',function(e) {
        e.stopPropagation();

        if (e.target !=  blob[0] || !opts['drag']) {
          slide.trigger('toggle', slide.hasClass('active'));
        }
      });
    }

    // we're done with all the non dragging stuff
    if (!opts['drag'] || selectType) return;

    // time to begin the dragging parts/blob clicks
    var diff;
    var slideLimit = (width - height) / 4;

    // fired on mouseup and mouseleave events
    var upLeave = function(e) {
      toggle.off('mousemove touchmove');
      slide.off('mouseleave');
      blob.off('mouseup touchend');

      var active = slide.hasClass('active');

      if (!diff && opts.click && e.type !== 'mouseleave') {

        // theres no diff so nothing has moved. only toggle if its a mouseup
        slide.trigger('toggle', active);
        return;
      }

      if (active) {

        // if the movement enough to toggle?
        if (diff < -slideLimit) {
          slide.trigger('toggle',active);
        } else {

          // go back
          inner.animate({
            marginLeft: 0
          },opts.animate/2);
        }
      } else {

        // inactive
        if (diff > slideLimit) {
          slide.trigger('toggle',active);
        } else {

          // go back again
          inner.animate({
            marginLeft: -width + height
          },opts.animate/2);
        }
      }

    };

    var wh = -width + height;

    blob.on('mousedown touchstart', function(e) {

      // reset diff
      diff = 0;

      blob.off('mouseup touchend');
      slide.off('mouseleave');
      var cursor = e.pageX;

      toggle.on('mousemove touchmove', blob, function(e) {
        diff = e.pageX - cursor;
        var marginLeft;
        if (slide.hasClass('active')) {

          marginLeft = diff;

          // keep it within the limits
          if (diff > 0) marginLeft = 0;
          if (diff < wh) marginLeft = wh;
        } else {

          marginLeft = diff + wh;

          if (diff < 0) marginLeft = wh;
          if (diff > -wh) marginLeft = 0;

        }

        inner.css('margin-left',marginLeft);
      });

      blob.on('mouseup touchend', upLeave);
      slide.on('mouseleave', upLeave);
    });


  });

};

/**
 * 拖动效果
 * $('#id').drags();
 */
$.fn.drags = function(opt) {
    opt = $.extend({
        handle: "",
        cursor: "move",
        draggableClass: "draggable",
        activeHandleClass: "active-handle"
    }, opt);

    var $selected = null;
    var $elements = (opt.handle === "") ? this : this.find(opt.handle);

    $elements.css('cursor', opt.cursor).on("mousedown", function(e) {
        if(opt.handle === "") {
            $selected = $(this);
            $selected.addClass(opt.draggableClass);
        } else {
            //$selected = $(this).parent().parent();
            $selected = $(this).parent();
            $selected.addClass(opt.draggableClass).find(opt.handle).addClass(opt.activeHandleClass);
        }
        var drg_h = $selected.outerHeight(),
            drg_w = $selected.outerWidth(),
            pos_y = $selected.offset().top + drg_h - e.pageY,
            pos_x = $selected.offset().left + drg_w - e.pageX;
        $(document).on("mousemove", function(e) {
            $selected.offset({
                top: e.pageY + pos_y - drg_h,
                left: e.pageX + pos_x - drg_w
            });
        }).on("mouseup", function() {
            $(this).off("mousemove"); // Unbind events from document
            if ($selected !== null) {
                $selected.removeClass(opt.draggableClass);
                $selected = null;
            }
        });
        e.preventDefault(); // disable selection
    }).on("mouseup", function() {
        if(opt.handle === "") {
            $selected.removeClass(opt.draggableClass);
        } else {
          if($selected) $selected.removeClass(opt.draggableClass)
                .find(opt.handle).removeClass(opt.activeHandleClass);
        }
        $selected = null;
    });
    return this;
};

/**
 *
 */
$.fn.stick = function(options){
  var pos = 'bottomleft'; var edge = 'topleft'; var rel = $(document.body);
  //var animate = false;
  // if need shadow, do shadow
  //if(options && options.animate) animate = options.animate;
  options = options || {}
  var animate = $chk(options.animate) == false ? false:true;
  if(options && options.modal && !$chk(this.shadow)) this.createShadow();
  if(options && options.position) pos = options.position;
  if(options && options.edge) edge = options.edge;
  if(options && options.relativeTo) rel = options.relativeTo;
  else if(options && options.event) rel = options.event.target || options.event.srcElement;
  if (rel[0] == $(document.body)[0]) { pos = 'center'; edge = 'center'; }
  //this.position({position:pos,edge:edge,relativeTo:rel});
  //this.css({position:"absolute", "z-index":"65520"}).appendTo($(rel))
  this.css({position:"absolute", "z-index":"65525"}).appendTo($(document.body))
  // this.css({position:"absolute", "z-index":"65520"}).appendTo($(document.body))
  // 设置元素relative位置
   var left = 0, top = 0;
   var direction = options.direction || "bottom";
   if (direction == 'bottom'){
     left = parseInt($(rel).css("width")) / 2 + $(rel).offset().left - parseInt(this.css("width")) / 2 - parseInt(this.css("margin-left"));
     top = parseInt($(rel).css("height")) + $(rel).offset().top;
   }
   if (direction == 'top'){
     left = parseInt($(rel).css("width")) / 2 + $(rel).offset().left - parseInt(this.css("width")) / 2 - parseInt(this.css("margin-left"));
     top = $(rel).offset().top - parseInt(this.css("height"));
   }
   if (direction == 'left'){
     left = $(rel).offset().left - parseInt(this.css("width"));
     top = parseInt($(rel).css("height")) / 2 + $(rel).offset().top - parseInt(this.css("height")) / 2;
   }
   if (direction == 'right'){
     left = parseInt($(rel).css("width")) + $(rel).offset().left;
     top = parseInt($(rel).css("height")) / 2 + $(rel).offset().top - parseInt(this.css("height")) / 2;
   }
  // 设置元素relative位置 ---- end 

  this.show();
  if(options && options.offset){
      if(options.offset.x) this.css("left", this.css('left').toInt() + options.offset.x + 'px');
      if(options.offset.y) this.css("top", this.css('top').toInt() + options.offset.y + 'px');
  }
  if (!options || !options.allowOutWindow) {
      // see if out of screen, if out, move it in the window
      var winscroll = {y:$(window).scrollTop(), x:$(window).scrollLeft()};
      var winsize = {x:$(window).width(), y:$(window).height()}
      var size = {width: parseInt(this.css("width")), height: parseInt(this.css("height"))}
      if (rel[0]!=$(document.body)[0]){
        var center_pos = {left:left, top:top}
      }else{
        var center_pos = {left:(winsize.x-parseInt(size.width))/2+winscroll.x-parseInt(this.css("margin-left")), top:(winsize.y-parseInt(size.height))/2+winscroll.y}
      }
      //var center_pos = {left:(winsize.x-winscroll.y-size.width)/2, top:(winsize.y-winscroll.y-size.height)/2}
      //if (animate == false){
        this.css(center_pos)
      //}else{
      //  this.css({top:winscroll.y-size.height, left:center_pos.left, opacity:"0.1"})
      //  this.animate({top:center_pos.top, left:center_pos.left, opacity:"1"}, "slow")
      //}
      var dim = {left:this.offset().left, top:this.offset().top, width:parseInt(this.css("width")), height:parseInt(this.css("height")), bottom:parseInt(this.css("height"))+this.offset().top, right:this.offset().left + parseInt(this.css("width"))}
      var pos = { x: center_pos.left, y: center_pos.top }; var chg_pos = false;
      if (dim.left < 0) { pos.x = 0; chg_pos = true; }
      //else if (dim.width < winsize.x && dim.right > winscroll.x + winsize.x) {
      else if (dim.width < winsize.x && dim.right > winscroll.x + winsize.x) {
              pos.x = winscroll.x + winsize.x - dim.width -5; chg_pos = true;
      }
      if(dim.top < 0){ pos.y = 0; chg_pos = true; }
      else if (dim.height < winsize.y && dim.bottom > winscroll.y + winsize.y) {
          // make sure the title bar in the window
          if (winsize.y > dim.height) pos.y = winscroll.y + winsize.y - dim.height;
          chg_pos = true;
      }
      if (chg_pos) {
        this.offset({left:pos.x,top:pos.y});
        center_pos = {left:pos.x,top:pos.y};
        //if (animate == false){
        //}else{
        //  this.css({top:"0px"})
        //  this.animate({top:pos.y, left:pos.x, opacity:"1"}, "slow")
        //}
      }
      if (animate==true){
        this.css({top:winscroll.y-size.height, left:center_pos.left, opacity:"0.1"})
        this.animate({top:center_pos.top, left:center_pos.left, opacity:"1"}, "slow")
      }
  }
  return this;
}
$.fn.createShadow = function(){
  var shadow = $(".gShadow");
  if (shadow.length > 0) return false;
  var shadow = $(document.createElement("div"))
  shadow.addClass("gShadow")
        .attr({style:'z-index:65520;background:#fff;filter:alpha(opacity=80);opacity:0.8;width:100%;height:100%;'})
        // .attr({style:'z-index:65520;background:#fff;filter:alpha(opacity=80);opacity:0.8;width:100%;height:100%;'})
  shadow.css('position','fixed'); shadow.css('left',0); shadow.css('top',0);
  shadow.css('display','none');
  shadow.appendTo($(document.body)); shadow.css('display',''); this.shadow = shadow;
  if ($isBrowser() == "IE") {
    //var winSize = window.getScrollSize();
    var winSize = {x:$(window).scrollTop(), y:$(window).scrollLeft()};
    var frm = $(document.createElement("iframe"))
    frm.addClass('gShadow').attr({style:"z-index:65520;position:absolute;top:0;left:0;filter:mask();width:100%;height:100%;"})

    //frm.css({ 'width':winSize.x, 'height':winSize.y });

    frm.appendTo($(document.body));
  }
}

$.fn.fshow = function(options){
  var options = options || {};
  var handle = null;
  if(options.handle) handle = options.handle;
  else if(options.handle_class) handle = this.find('.' + options.handle_class);
  else handle = this.find('.title');
  var rel = $(document.body);
  if(options.relativeTo) rel = options.relativeTo;
  if(options.event) rel = options.event.target || options.event.srcElement;
  // check if is child of body, if not, move to body
  var parent = this.parent();
  if(!$ifBody(parent)) this.appendTo($(document.body));
  options.relativeTo = rel;
  this.stick(options);
  //if($chk2(handle)) var dragg = new Draggable({handle:handle,container:this});
  if (options.drag_handle) $(this).drags({handle:options.drag_handle});
  var self = this;
  $(document).bind("keypress", function(event){
    if (event && event.keyCode == 27 || event && event.type=="click"){
      $(document).unbind("keypress", self.tHide())
      self.tHide(options);
    }
  })
}

$.fn.tClose = function(options){
  options = options || {};
  var animate = $chk(options.animate) == false ? true:false;
  var self = this;
  if (animate == true){
    this.animate({top:"0px", opacity:"0"}, "slow", function(){self.remove();})
  }else{
    this.remove();
  }
  try{
    delete this;
    $(".modal-backdrop").remove();
    delete $('.modal-backdrop');
    $("body").removeClass("modal-open")
  }catch(e){}
  try{
    $(".gShadow").remove();
    delete $(".gShadow");
    $("div.gShadow").remove();
    delete $("div.gShadow");
    $(window.top.document).find(".gShadow").remove();
    delete $(window.top.document).find(".gShadow");
  }catch(e){}
}

$.fn.tHide = function(options){
  //this.css("display", "none");
  var self = this;
  options = options || {};
  var animate = $chk(options.animate) == false ? false:true;
  var self = this;
  if (animate == true){
    this.animate({opacity:"0"}, "fast", function(){self.css("display", "none");})
  }else{
    this.css({"display": "none"})
  }
  try{
    delete this;
    $(".modal-backdrop").remove();
    delete $('.modal-backdrop');
  }catch(e){}
  try{
    $(".gShadow").remove();
    delete $(".gShadow");
    $("div.gShadow").remove();
    delete $("div.gShadow");
  }catch(e){}
}

$.fn.tShow = function(){
  this.css("display", "block");
}

$.fn.tLoading = function(_loading_text){
  this.attr("disabled", "disabled");
  this.css("opacity", "0.5")
  text = this.text() || this.val()
  this.attr("origin_text", text)
  loading_text = this.attr("loading_text") || "loading..."
  if (_loading_text) loading_text = _loading_text;
  try{
    this.text(loading_text)
  }catch(e){
    this.attr("text", loading_text)
  }
  this.val(loading_text)
  try{
    if (this[0].tagName.toLowerCase() == "a"){
      if( $(this).css("display") == "none" ) return false;
      this.html(loading_text)
      var dom = $(document.createElement('a'));
      dom.css(this.attr("style"))
      dom.css("opacity", "0.5")
      dom.attr("class", this.attr("class"))
      dom.html(loading_text)
      //this.after("<a href='javascript:;'>"+loading_text+"</a>")
      this.after(dom)
      this.css('display', 'none');
    }
  }catch(e){}
}

$.fn.tReset = function(_reset_text){
  this.removeAttr("disabled")
  this.css("opacity", "")
  reset_text = this.attr("reset_text") || "complete"
  if (_reset_text) reset_text = _reset_text
  try{
    this.text(reset_text)
  }catch(e){
    this.attr("text", reset_text)
  }
  this.val(this.attr("origin_text"))
  try{
    if (this[0].tagName.toLowerCase() == "a"){
      this.next().remove()
      this.css('display', '');
    }
  }catch(e){}
}

$.fn.tComplete = function(_complete_text){
  this.removeAttr("disabled")
  this.css("opacity", "")
  complete_text = this.attr("complete_text") || "complete"
  if (_complete_text) complete_text = _complete_text
  try{
    this.text(complete_text)
  }catch(e){
    this.attr("text", complete_text)
  }
  this.val(complete_text)
  try{
    if (this[0].tagName.toLowerCase() == "a"){
      this.next().remove()
      this.css('display', '');
    }
  }catch(e){}
}


/**
 * ***************************************************************************************************
 * 自定义扩展函数 (custom functions)
 * ***************************************************************************************************
 */
$isBrowser = function(){ 
    var Sys = {};
    var ua = navigator.userAgent.toLowerCase();
    var s;
    (s = ua.match(/msie ([\d.]+)/)) ? Sys.ie = s[1] :
    (s = ua.match(/firefox\/([\d.]+)/)) ? Sys.firefox = s[1] :
    (s = ua.match(/chrome\/([\d.]+)/)) ? Sys.chrome = s[1] :
    (s = ua.match(/opera.([\d.]+)/)) ? Sys.opera = s[1] :
    (s = ua.match(/version\/([\d.]+).*safari/)) ? Sys.safari = s[1] : 0;

    if (Sys.ie) return "IE";
    if (Sys.firefox) return "FIREFOX"; 
    if (Sys.chrome) return "CHROME";
    if (Sys.opera) return "OPERA";
    if (Sys.safari) return "SAFARI"; 
} 

$chk = function(obj){
  if(obj == undefined) return false;
  if(obj == null) return false;
  if(obj == '') return false;
  return !!(obj || obj === 0)
}
$defined = function(arg){
  return !(typeof(arg) == 'undefined');
};
function $ifBody(element){
  if(!$chk(element)) return false;
  return (/^(?:body|html)$/i).test(element.tagName);
}
$checkAll = function(parent, chkall){
    var childs = $(parent).find("input");
    for (var i = 0; i < childs.length; i++) {
    if($chk(childs[i].type) && childs[i].type=='checkbox')
          $(childs[i]).prop("checked", $(chkall).prop("checked"));
    }
}
$getCheckIds = function(parent, exclude_chkall){
    var ptable = $(parent); var ids = []; exclude_chkall = $(exclude_chkall);
    var childs = ptable.find("input");
    for (var i = 0; i < childs.length; i++) {
      var child = $(childs[i]);
      if($chk(exclude_chkall)){
        if (child.prop("checked") == true && child[0] != exclude_chkall[0])  ids.push(child.prop("id"));
      }else{
        if (child.prop("checked") == true)  ids.push(child.prop("id"));
      }
    }
    return ids;
}
$getCheckValues = function(parent, exclude_chkall){
    var ptable = $(parent); var vals = []; exclude_chkall = $(exclude_chkall);
    var childs = ptable.find("input");
    for (var i = 0; i < childs.length; i++) {
      var child = $(childs[i]);
      if($chk(exclude_chkall)){
        if (child.prop("checked") == true && child[0] != exclude_chkall[0])  vals.push(child.val());
      }else{
        if (child.prop("checked") == true)  vals.push(child.val());
      }
    }
    return vals;
}
$getChkVals = function(parent, chkall){
    var ptable = $(parent); var ids = []; chkall = $(chkall);
    var childs = ptable.find("input");
    for (var i = 0; i < childs.length; i++) {
      var child = $(childs[i]);
      if($chk(chkall)){
        if (child.prop("checked") == true && child != chkall)  ids.push(child.val());
      }else{
        if (child.prop("checked") == true)  ids.push(child.val());
      }
    }
    return ids;
}
$generateId = function(options){
  options = options || {}
  var _length = 5;
  var _randomStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
  var random_id = "";
  if ($defined(options.length) && options.length>=0) _length = options.length;
  if ($defined(options.randomStr) && options.randomStr!='') _randomStr = options.randomStr;
  for( var i=0; i < _length; i++ )
      random_id += _randomStr.charAt(Math.floor(Math.random() * _randomStr.length));
  return random_id;
};
$GenerateId = function(options){ return new $GenerateId.fn.init(options); }; $GenerateId.fn = $GenerateId.prototype = {
  _options: null, _length: 5, 
  _randomStr: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
  _randomInt: '1234567890',
  random_id: "",
  init: function(options){
    options = options || {}
    this._options = options;
    if ($defined(options.length) && options.length>=0) this._options.length = this._length = options.length;
    if ($defined(options.randomStr) && options.randomStr!='') this._options.randomStr = this._randomStr = options.randomStr;
  },
  generateStr: function(){
    for( var i=0; i < this._length; i++ )
        this.random_id += this._randomStr.charAt(Math.floor(Math.random() * this._randomStr.length));
    return this.random_id;
  },
  generateNum: function(){
    for( var i=0; i < this._length; i++ )
        this.random_id += this._randomInt.charAt(Math.floor(Math.random() * this._randomInt.length));
    return parseInt(this.random_id);
  }
}; $GenerateId.fn.init.prototype = $GenerateId.fn;

$cookie = function(name, value, options) {
  if (typeof value != 'undefined') {
    options = options || {};
    if (value === null) {
      value = '';
      options = $.extend({}, options);
      options.expires = -1;
    }
    var expires = '';
    if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
      var date;
      if (typeof options.expires == 'number') {
        date = new Date();
        date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
      } else {
        date = options.expires;
      }
      expires = '; expires=' + date.toUTCString();
    }
    var path = options.path ? '; path=' + (options.path) : '';
    var domain = options.domain ? '; domain=' + (options.domain) : '';
    var secure = options.secure ? '; secure' : '';
    document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
    } else {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
};

$removeCookie = function(name){
  document.cookie = name + '=; expires=Thu, 01-Jan-70 00:00:01 GMT;';
}

/**
 * ***************************************************************************************************
 * 扩展自定义类 (custom classes)
 * ***************************************************************************************************
 */

/**
 * 弹出框
 * $MsgBox({appendTo:"div.container.theme-showcase").show();
 */
$MsgBox = function(options){ return new $MsgBox.fn.init(options); }; $MsgBox.fn = $MsgBox.prototype = {
  _options: {}, _id: null, _title: null, _message: null, _appendTo: null, _buttons:[], _footer: "show", _closeBtn: "show",
  _modal_dialog: null, _moveSpeed: null, _backdrop: 'static',
  /**
   * init options
   */
  init: function(options){
    options = options || {}
    this._options = options || {};
    this._id = this._options.id = options.id || $GenerateId().generateStr();
    this._message = this._options.message = options.message || "";
    this._title = this._options.title = options.title || "消息提示";
    this._appendTo = this._options.appendTo = options.appendTo || "div.container";
    this._moveSpeed = this._options.moveSpeed = options.moveSpeed || null;
    this._backdrop = this._options.backdrop = options.backdrop || 'static';
    this._buttons = this._options.buttons = options.buttons || [];
    this._footer = this._options.footer = options.footer || "show";
    this._closeBtn = this._options.closeBtn = options.closeBtn || "show";
    this._shadow = this._options.shadow = options.shadow || "show";
    this.createBox();
    return this;
  },
  /**
   * 生成对话框
   */
  createBox: function(){
    var self = this;
    if($chk($("#"+this._id)[0])) return this;
    var modal_dialog = document.createElement("div");
    $(modal_dialog).attr({id:this._id, style:"display:none"}).addClass("modal-dialog").appendTo($(document.body));
    var modal_content = document.createElement("div");
      $(modal_content).addClass("modal-content").appendTo($(modal_dialog));
    var modal_header = document.createElement("div");
      $(modal_header).addClass("modal-header").appendTo($(modal_content));
    $(modal_dialog).drags({handle:modal_header});
    if(this._closeBtn == "show"){
      var button = document.createElement("button");
      $(button).addClass("close")
            .text("×")
            .bind("click", function(){
              $("#"+self._id).tClose();
            })
            .appendTo($(modal_header));
    }
    var h4 = document.createElement("h4");
    $(h4).addClass("modal-title")
          .attr({id:"myModalLabel"})
          .text(this._options.title)
          .appendTo($(modal_header));
    var modal_body = document.createElement("div");
      $(modal_body).addClass("modal-body").html(this._options.message).appendTo($(modal_content));
    if (this._footer == "show"){
      var modal_footer = document.createElement("div");
        $(modal_footer).addClass("modal-footer").appendTo($(modal_content));
    }
    this._modal_dialog = $(modal_dialog);
    this.appendButtons(this._buttons);
    return this;
  },
  /**
   * 设置标题
   */
  setTitle: function(_title){
    this._modal_dialog.find(".modal-title").html(_title);
    return this;
  },
  appendButtons: function(buttons){
    try{this._modal_dialog.find('div.modal-footer').find("button").remove()}catch(e){}
    var button_close = document.createElement("button");
    var modal_footer = this._modal_dialog.find('div.modal-footer');
    if (buttons.length > 0){
      for(var i=0;i<buttons.length;i++){
        var btn = buttons[i];
        var button = document.createElement("button");
        var btn_id = btn.id || $GenerateId().generateStr();
        var loading_text = btn.loading_text || "";
        $(button).addClass("btn btn-primary")
              .attr({type:"button", id:btn_id, "data-loading-text":loading_text})
              .text(btn.text)
              .bind("click", btn.action)
              .appendTo($(modal_footer));
      }
    }else{
      modal_footer.css("display", "none");
    }
    return this;
  },
  /**
   * 设置内容
   */
  setHtml: function(_html){
    this._modal_dialog.find(".modal-body").html(_html);
    return this;
  },
  fillHtml:function(_html){
    this._modal_dialog.find(".modal-header").after(_html);
    return this;
  },
  /**
   * 显示弹出框
   */
  show: function(opts){
    var self = this;
    opts = $.extend({modal:true, animate:true}, opts)
    $('#'+this._options.id).fshow(opts);
  }
}; $MsgBox.fn.init.prototype = $MsgBox.fn;


/**
 * 工具提示窗口
 * ToolBox
 */
$ToolBox = function(options){ return new $ToolBox.fn.init(options); }; $ToolBox.fn = $ToolBox.prototype = {
  _options: {}, _id: null, _title: null, _message: null, _appendTo: null, _direction: null, _html: null, _buttons:[],
  _toolbox_dialog: null, _stick: false, _arrow: false,
  init: function(options){
    options = options || {};
    this._options = options || {};
    var self = this;
    var _generate_id = $GenerateId({length:10}).generateStr();
    this._id = this._options.id = options.id || _generate_id;
    this._message = this._options.message = options.message || "";
    this._html = this._options.html = options.html || "";
    this._title = this._options.title = options.title || "Title";
    this._appendTo = this._options.appendTo = options.appendTo || "";
    this._direction = this._options.direction = this._options.placement = options.direction || options.placement || "bottom";
    this._stick = this._options.stick = options.stick || false;
    this._arrow = this._options.arrow = options.arrow || false;
    this._buttons = this._options.buttons = options.buttons || [];
    this._styles = this._options.styles = options.styles || {};
    this._onHide = this._options.onHide = options.onHide || null;
    this.createBox();
    return this;
  },
  createBox: function(){
    var self = this;
    $(document).bind("keypress", function(event){
          self.tHide(event)
          //self.onHide();
          //$("#"+self._id).tHide();
    })
    if($chk($("#"+this._id)[0])) return this;
    this._toolbox_dialog = $(document.createElement("div")).addClass("popover")
                            .attr({"style":"display:none", "id":this._id}).appendTo("body");
    this._toolbox_arrow = $(document.createElement("div")).addClass("arrow")
                            .attr({"style":"display:none"});
    this._toolbox_title = $(document.createElement("h3")).addClass("popover-title")
                                .attr({style:"cursor:move"}).appendTo(this._toolbox_dialog);
    $(document.createElement("span")).appendTo(this._toolbox_title)
    $(document.createElement("button")).addClass("tipclose")
          .text("×")
          .bind("click", function(event){
              self.tHide(event)
              //self.onHide();
              //$("#"+self._id).tHide();
          })
          .appendTo(this._toolbox_title);
    this.appendButtons(this._buttons);
    this._toolbox_content = $(document.createElement("div")).addClass("popover-content").appendTo(this._toolbox_dialog)
    $(document.createElement("p")).attr({name:"content", style:"padding:5px"}).appendTo(this._toolbox_content)
    this._content_buttons = $(document.createElement("div")).attr({style:"margin-bottom:0px"}).addClass("form-group").appendTo(this._toolbox_content)
    $(document.createElement("div")).attr({name:"buttons"}).addClass("col-sm-offset-4").addClass("col-sm-8").appendTo(this._content_buttons)
    $('#'+this._id).find('h3.popover-title span').text(this._title);
    $('#'+this._id).find('div.popover-content p[name=content]').html(this._message);
    if(self._html){
      self.setHtml(self._html)
    }
    this.appendButtons(this._buttons);
  },
  setTitle: function(_title){
    $('#'+this._id).find('h3.popover-title span').text(_title);
    return this;
  },
  setHtml: function(_html){
    $('#'+this._id).find('div.popover-content p[name=content]').html(_html);
    return this;
  },
  appendButtons: function(buttons){
    var self = this;
    $('#'+this._id).find('div[name=buttons]').html('');
    for(var i=0; i<=buttons.length; i++){
      if(buttons[i]==null) break;
      var text = buttons[i].text;
      var action = buttons[i].action;
      var id = buttons[i].id || Math.random();
      var ele = $(document.createElement('button'));
          ele.attr({
        'class': 'btn btn-warning',
        "loading_text":"正在提交",
        "complete_text": "确定",
        id: id,
        value: text,
      }).bind("click", action).html(text)
      $('#'+this._id).find('div[name=buttons]').append(ele);
      $('#'+this._id).find('div[name=buttons]').append("&nbsp;");
    }
    return this;
  },
  tHide:function(event){
    var self = this;
    if (!$defined(event)) return
    if (event && event.keyCode == 27 || event && event.type=="click"){
      self.onHide();
      $(document).unbind("keypress", this.tHide())
      $("#"+self._id).tHide();
    }
  },
  onHide: function(){if(this._onHide)(this._onHide)()},
  show: function(opts){
    var self = this;
    this._options = $.extend({drag_handle:$('#{0} .popover-title'.format(this._id)), modal:true}, opts)
    $("#"+this._id).fshow(this._options)
    //return this;
  }
}; $ToolBox.fn.init.prototype = $ToolBox.fn;

/**
 * 警告窗口
 * AlertBox
 */
$AlertBox = function(options){ return new $AlertBox.fn.init(options); }; $AlertBox.fn = $AlertBox.prototype = {
  _options: null, id: null, _alert: "alert-warning", _opacity: 1, _appendTo: null, _html: null, _onClose: null,
  _alert_box: null, _buttons:[],
  init: function(options){
    options = options || {};
    self = this;
    this._options = options || {};
    this._id = this._options.id = options.id || null;
    this._alert = this._options.alert = options.alert || "alert-warning";
    this._opacity = this._options.opacity = options.opacity || 1;
    this._html = this._options.html = options.html || "&nbsp;";
    this._appendTo = this._options.appendTo = options.appendTo || "";
    this._buttons = this._options.buttons = options.buttons || [];
    this._onClose = this._options.onClose = options.onClose || null;
    this._dragable = this._options.draggable = options.draggable || false;
    this.createBox();
    return this;
  },
  createBox: function(){
    //var self = this;
    //if($chk($("#"+this._id)[0])) return self;
    var div = $(document.createElement("div"));
    if (this._dragable) div.drags();
    div.addClass("alert "+ this._alert + " fade in")
        .css({opacity:this._opacity})
    if (this._id)
        div.attr({id:self._id})
    var close_button = document.createElement("button");
    $(close_button).addClass("close")
          .attr({type:"button", 
                 "data-dismiss":"alert", 
                 "aria-hidden":"true"})
          .text("×")
          .appendTo(div);
    var alert_content = $(document.createElement("div"));
    alert_content.attr({name:"alert_content"}).html(this._html);
    alert_content.appendTo(div)
    div.appendTo(this._appendTo)
    this._alert_box = div;
    this._alert_box.css("display", "none");
    this.appendButtons(this._buttons);
    return this;
  },
  appendButtons: function(buttons){
    try{this._alert_box.find("div[name=alert_content] #alert_buttons").remove()}catch(e){}
    var alert_content = this._alert_box.find("div[name=alert_content]").append("<div id='alert_buttons'>")
    //for (var btn in this._buttons){
    for (var i in buttons){
      var btn = buttons[i];
      var _btn = document.createElement("button");
      $(_btn).addClass("btn btn-primary")
            .attr({type:"button"})
            .text(btn.text)
            //.bind("click", function(){ (btn.action)(); })
            .bind("click", btn.action)
            //.appendTo(alert_content);
      alert_content.find("#alert_buttons").append($(_btn))
    }
    return this;
  },
  setHtml: function(_html){
    this._alert_box.find("div[name=alerted]").html(_html);
    return this;
  },
  show: function(){
    this._alert_box.css("display", "block");
    return this;
  },
  tHide: function(){
    self = this;
    this._alert_box.css("display", "none");
    if (this._onClose){
      (self._onClose)();
    }
    return this;
  },
  tClose: function(){
    self = this;
    this._alert_box.remove();
    if (this._onClose){
      (self._onClose)();
    }
    return this;
  },
  onClose: function(){
    self = this;
    if (this._onClose){
      (self._onClose)();
    }
    return this;
  }
}; $AlertBox.fn.init.prototype = $AlertBox.fn;


/**
 * ParamsBox
 */
$ParamsBox = function(options){ return new $ParamsBox.fn.init(options); }; $ParamsBox.fn = $ParamsBox.prototype = {
    _options:{}, _autoFire:true, _controls:[], _submitButtons:[], _extraParams:'',
    init: function(options){
        options = options || {};
        //if(!options || !options.controls) return;
        this._options = options;
        this._controls = options.controls; 
        //if(this._controls.length==0) return;
        if(options.submitButtons) this._submitButtons = options.submitButtons;
        if(options.autoFire) this._autoFire = options.autoFire;
        if(options.extraParams) this._extraParams = options.extraParams;
        this.attachEvt(); this.loadUrl();
    },
    attachEvt: function(){
        var self = this;
        var uls = this._controls;
        for(var i=0;i<uls.length;i++){
            // link buttons
            var lnks = $(uls[i]).find('a');
            for(var j=0;j<lnks.length;j++) {
                //if(!this._submitButtons.contains(lnks[j]))
                $(lnks[j]).bind('click',function(event){ self.checkMe(event); });
            }
            // input text control
            var inputs = $(uls[i]).find('input');
            for(var j=0;j<inputs.length;j++) {
                //if(!this._submitButtons.contains(inputs[j]))
                $(inputs[j]).bind('click',function(event){ self.checkMe(event); });
            }
        }
        if(this._submitButtons.length > 0)
          for(var j=0; j<this._submitButtons.length; j++){
            //this._submitButtons.each(function(item){
                var item = this._submitButtons[j]
                if(item && item[0].type=='button') item.bind('click',function(){ self.goUrl(); });
                // 给文本框增加回车即查询功能
                if(item && item[0].type=='text'){
                    item.bind('keydown',function(event){
                        if(event.keyCode == 13 && !event.ctrlKey && !event.shiftKey && !event.altKey){
                            self.goUrl();
                        }
                    });
                }
            };
    },
    loadUrl: function(){
        // initial all selections
        var uls = this._controls;
        for(var i=0;i<uls.length;i++) this.setState($(uls[i]).get('id'));
        // set url parameters
        var search = window.location.search.replace('?','');
        var params = search.parseQueryString();
        for(var item in params){
          this.setState(item,params[item]);
        }
    },
    getOtherUrl: function(obj){
        if(!$defined(obj)) return;if(!obj) return ''; obj = $(obj); if(!obj) return ''; var ret = '';
        if (obj.tagName.toLowerCase() != 'input') {
            var links = obj.find('a');
            for (var i = 0; i < links.length; i++) {
                if ($(links[i].parentNode).hasClass('active')) {
                    ret = links[i].get('eurl'); break;
                }
            }
        }else if(obj.type=='text' || obj.type=='hidden' || obj.type==''){
            ret = obj.get('eurl');
        }
        if(!$chk(ret)) ret = '';
        return ret;
    },
    getState: function(obj){
        if(!$defined(obj)) return;if(!obj) return '-1'; obj = $("#"+obj); if(!obj) return '-1'; var ret = '-1';
        if (obj[0].tagName.toLowerCase() != 'input') {
            var links = obj.find('a');
            for (var i = 0; i < links.length; i++) {
                if ($(links[i].parentNode).hasClass('active')) {
                    ret = $(links[i]).attr('evalue'); break;
                }
            }
        //}else if(obj.attr("type")=='text' || obj.attr("type")=='hidden' || obj.attr("type")==''){
        }else if(obj[0].type=='text' || obj[0].type=='hidden' || obj[0].type==''){
          ret = obj.val();
        }
        return ret;
    },
    setState: function(obj,value){
      if(!$defined(obj)) return;if(!obj) return; obj = $("#"+obj); if(obj.length == 0) return; if(!obj) return;
        if(obj[0].tagName.toLowerCase() != 'input'){
            if(!$defined(value)) value = '-1';
            value = value + '';
            var links = obj.find('a');
            for(var i=0;i<links.length;i++){
              if ($(links[i]).attr('evalue') == value) {
                $(links[i]).parent().addClass('active');
              } else {
                $(links[i]).parent().removeClass('active');
              }
            }
        }else{
          if (obj.attr("type") == 'text' || obj.attr("type") == 'hidden' || obj.attr("type") == '') {
            if($chk(value)) obj.val(value);
                else obj.val("");
            }
        }
    },
    checkMe: function(ev){
        ev = ev || window.event;
        var element = ev.target || ev.srcElement;
        var parent = element.parentNode.parentNode;
        var links = parent.getElementsByTagName('a');
        for(var i=0;i<links.length;i++){
            if(links[i] == element) $(links[i].parentNode).addClass('active');
            else $(links[i].parentNode).removeClass('active');
        }
        // connect to sub elements
        var uls = this._controls; var id = $(parent).attr('id');
        if($chk(id)){
            for (var i = 0; i < uls.length; i++) {
              var pname = $(uls[i]).attr('eparent');
                if($chk(pname) && pname == id){
                    //this.setState(uls[i],-1);
                    this.setState($(uls[i]).attr("id"),-1);
                }
            }
        }

        if(this._autoFire)  this.goUrl();
        ev.returnValue = false;
        if(window.event) window.event.returnValue = false;
    },
    getQueryString: function(params){
      var result = [];
      for (var item in params){
        result.push("{0}={1}".format(item, params[item]));
      }
      return result.join("&");
    },
    goUrl: function(){
        var url = window.location.href.replace(window.location.search,'');
        var params = new Object(); var uls = this._controls;
        var par = this._extraParams.parseQueryString();
        for(var i in par){ 
          if($chk(i)) 
            params[i] = par[i];
        }
        //params = this._extraParams.parseQueryString();
        for(var i=0;i<uls.length;i++){
          var id = $(uls[i]).attr('id'); params[id] = this.getState(id);
          if(url=='') url = this.getOtherUrl(id);
        }
        //var _uri = url.toURI();
        //_uri.setData(params,true);
        var _uri = "{0}?{1}".format(url, this.getQueryString(params))
        window.location.href = _uri;
    }
}; $ParamsBox.fn.init.prototype = $ParamsBox.fn;

$StateBox = function(options){ return new $StateBox.fn.init(options); }; $StateBox.fn = $StateBox.prototype = {
    _options:{}, _autoFire:true, _controls:[], _submitButtons:[], _extraParams:'',
    init: function(options){
        options = options || {};
        //if(!options || !options.controls) return;
        this._options = options;
        this._controls = options.controls; 
        this.loadUrl();
    },
    attachEvt: function(){
        var self = this;
        var uls = this._controls;
        for(var i=0;i<uls.length;i++){
            // link buttons
            var lnks = $(uls[i]).find('a');
            for(var j=0;j<lnks.length;j++) {
                //if(!this._submitButtons.contains(lnks[j]))
                $(lnks[j]).bind('click',function(event){ self.checkMe(event); });
            }
            // input text control
            var inputs = $(uls[i]).find('input');
            for(var j=0;j<inputs.length;j++) {
                //if(!this._submitButtons.contains(inputs[j]))
                $(inputs[j]).bind('click',function(event){ self.checkMe(event); });
            }
        }
        if(this._submitButtons.length > 0)
          for(var j=0; j<this._submitButtons.length; j++){
            //this._submitButtons.each(function(item){
                var item = this._submitButtons[j]
                if(item && item[0].type=='button') item.bind('click',function(){ self.goUrl(); });
                // 给文本框增加回车即查询功能
                if(item && item[0].type=='text'){
                    item.bind('keydown',function(event){
                        if(event.keyCode == 13 && !event.ctrlKey && !event.shiftKey && !event.altKey){
                            self.goUrl();
                        }
                    });
                }
            };
    },
    loadUrl: function(){
        // initial all selections
        var uls = this._controls;
        for(var i=0;i<uls.length;i++) this.setState($(uls[i]).get('id'));
        // set url parameters
        var search = window.location.search.replace('?','');
        var params = search.parseQueryString();
        for(var item in params){
          this.setState(item,params[item]);
        }
    },
    getOtherUrl: function(obj){
        if(!$defined(obj)) return;if(!obj) return ''; obj = $(obj); if(!obj) return ''; var ret = '';
        if (obj.tagName.toLowerCase() != 'input') {
            var links = obj.find('a');
            for (var i = 0; i < links.length; i++) {
                if ($(links[i].parentNode).hasClass('active')) {
                    ret = links[i].get('eurl'); break;
                }
            }
        }else if(obj.type=='text' || obj.type=='hidden' || obj.type==''){
            ret = obj.get('eurl');
        }
        if(!$chk(ret)) ret = '';
        return ret;
    },
    getState: function(obj){
        if(!$defined(obj)) return;if(!obj) return '-1'; obj = $("#"+obj); if(!obj) return '-1'; var ret = '-1';
        if (obj[0].tagName.toLowerCase() != 'input') {
            var links = obj.find('a');
            for (var i = 0; i < links.length; i++) {
                if ($(links[i].parentNode).hasClass('active')) {
                    ret = $(links[i]).attr('evalue'); break;
                }
            }
        //}else if(obj.attr("type")=='text' || obj.attr("type")=='hidden' || obj.attr("type")==''){
        }else if(obj[0].type=='text' || obj[0].type=='hidden' || obj[0].type==''){
          ret = obj.val();
        }
        return ret;
    },
    setState: function(obj,value){
      if(!$defined(obj)) return;if(!obj) return; obj = $("#"+obj); if(obj.length == 0) return; if(!obj) return;
        if(obj[0].tagName.toLowerCase() != 'input'){
            if(!$defined(value)) value = '-1';
            value = value + '';
            var links = obj.find('a');
            for(var i=0;i<links.length;i++){
              if ($(links[i]).attr('evalue') == value) {
                $(links[i]).parent().addClass('active');
              } else {
                $(links[i]).parent().removeClass('active');
              }
            }
        }else{
          if (obj.attr("type") == 'text' || obj.attr("type") == 'hidden' || obj.attr("type") == '') {
            if($chk(value)) obj.val(value);
                else obj.val("");
            }
        }
    },
    checkMe: function(ev){
        ev = ev || window.event;
        var element = ev.target || ev.srcElement;
        // var parent = element.parent().parent();
        var links = element.getElementsByTagName('a');
        for(var i=0;i<links.length;i++){
            if(links[i] == element) $(links[i].parent()).addClass('active');
            else $(links[i].parent()).removeClass('active');
        }
        // connect to sub elements
        var uls = this._controls; var id = $(parent).attr('id');
        if($chk(id)){
            for (var i = 0; i < uls.length; i++) {
              var pname = $(uls[i]).attr('eparent');
                if($chk(pname) && pname == id){
                    //this.setState(uls[i],-1);
                    this.setState($(uls[i]).attr("id"),-1);
                }
            }
        }

        if(this._autoFire)  this.goUrl();
        ev.returnValue = false;
        if(window.event) window.event.returnValue = false;
    },
    getQueryString: function(params){
      var result = [];
      for (var item in params){
        result.push("{0}={1}".format(item, params[item]));
      }
      return result.join("&");
    },
    goUrl: function(){
        var url = window.location.href.replace(window.location.search,'');
        var params = new Object(); var uls = this._controls;
        var par = this._extraParams.parseQueryString();
        for(var i in par){ 
          if($chk(i)) 
            params[i] = par[i];
        }
        //params = this._extraParams.parseQueryString();
        for(var i=0;i<uls.length;i++){
          var id = $(uls[i]).attr('id'); params[id] = this.getState(id);
          if(url=='') url = this.getOtherUrl(id);
        }
        //var _uri = url.toURI();
        //_uri.setData(params,true);
        var _uri = "{0}?{1}".format(url, this.getQueryString(params))
        window.location.href = _uri;
    }
}; $StateBox.fn.init.prototype = $StateBox.fn;

})(jQuery);

/**
*
*  Secure Hash Algorithm (SHA1)
*  http://www.webtoolkit.info/
*
**/
 
//function SHA1 (msg) {
var SHA1 = function (msg) {
 
  function rotate_left(n,s) {
    var t4 = ( n<<s ) | (n>>>(32-s));
    return t4;
  };
 
  function lsb_hex(val) {
    var str="";
    var i;
    var vh;
    var vl;
 
    for( i=0; i<=6; i+=2 ) {
      vh = (val>>>(i*4+4))&0x0f;
      vl = (val>>>(i*4))&0x0f;
      str += vh.toString(16) + vl.toString(16);
    }
    return str;
  };
 
  function cvt_hex(val) {
    var str="";
    var i;
    var v;
 
    for( i=7; i>=0; i-- ) {
      v = (val>>>(i*4))&0x0f;
      str += v.toString(16);
    }
    return str;
  };
 
 
  function Utf8Encode(string) {
    string = string.replace(/\r\n/g,"\n");
    var utftext = "";
 
    for (var n = 0; n < string.length; n++) {
 
      var c = string.charCodeAt(n);
 
      if (c < 128) {
        utftext += String.fromCharCode(c);
      }
      else if((c > 127) && (c < 2048)) {
        utftext += String.fromCharCode((c >> 6) | 192);
        utftext += String.fromCharCode((c & 63) | 128);
      }
      else {
        utftext += String.fromCharCode((c >> 12) | 224);
        utftext += String.fromCharCode(((c >> 6) & 63) | 128);
        utftext += String.fromCharCode((c & 63) | 128);
      }
 
    }
 
    return utftext;
  };
 
  var blockstart;
  var i, j;
  var W = new Array(80);
  var H0 = 0x67452301;
  var H1 = 0xEFCDAB89;
  var H2 = 0x98BADCFE;
  var H3 = 0x10325476;
  var H4 = 0xC3D2E1F0;
  var A, B, C, D, E;
  var temp;
 
  msg = Utf8Encode(msg);
 
  var msg_len = msg.length;
 
  var word_array = new Array();
  for( i=0; i<msg_len-3; i+=4 ) {
    j = msg.charCodeAt(i)<<24 | msg.charCodeAt(i+1)<<16 |
    msg.charCodeAt(i+2)<<8 | msg.charCodeAt(i+3);
    word_array.push( j );
  }
 
  switch( msg_len % 4 ) {
    case 0:
      i = 0x080000000;
    break;
    case 1:
      i = msg.charCodeAt(msg_len-1)<<24 | 0x0800000;
    break;
 
    case 2:
      i = msg.charCodeAt(msg_len-2)<<24 | msg.charCodeAt(msg_len-1)<<16 | 0x08000;
    break;
 
    case 3:
      i = msg.charCodeAt(msg_len-3)<<24 | msg.charCodeAt(msg_len-2)<<16 | msg.charCodeAt(msg_len-1)<<8  | 0x80;
    break;
  }
 
  word_array.push( i );
 
  while( (word_array.length % 16) != 14 ) word_array.push( 0 );
 
  word_array.push( msg_len>>>29 );
  word_array.push( (msg_len<<3)&0x0ffffffff );
 
 
  for ( blockstart=0; blockstart<word_array.length; blockstart+=16 ) {
 
    for( i=0; i<16; i++ ) W[i] = word_array[blockstart+i];
    for( i=16; i<=79; i++ ) W[i] = rotate_left(W[i-3] ^ W[i-8] ^ W[i-14] ^ W[i-16], 1);
 
    A = H0;
    B = H1;
    C = H2;
    D = H3;
    E = H4;
 
    for( i= 0; i<=19; i++ ) {
      temp = (rotate_left(A,5) + ((B&C) | (~B&D)) + E + W[i] + 0x5A827999) & 0x0ffffffff;
      E = D;
      D = C;
      C = rotate_left(B,30);
      B = A;
      A = temp;
    }
 
    for( i=20; i<=39; i++ ) {
      temp = (rotate_left(A,5) + (B ^ C ^ D) + E + W[i] + 0x6ED9EBA1) & 0x0ffffffff;
      E = D;
      D = C;
      C = rotate_left(B,30);
      B = A;
      A = temp;
    }
 
    for( i=40; i<=59; i++ ) {
      temp = (rotate_left(A,5) + ((B&C) | (B&D) | (C&D)) + E + W[i] + 0x8F1BBCDC) & 0x0ffffffff;
      E = D;
      D = C;
      C = rotate_left(B,30);
      B = A;
      A = temp;
    }
 
    for( i=60; i<=79; i++ ) {
      temp = (rotate_left(A,5) + (B ^ C ^ D) + E + W[i] + 0xCA62C1D6) & 0x0ffffffff;
      E = D;
      D = C;
      C = rotate_left(B,30);
      B = A;
      A = temp;
    }
 
    H0 = (H0 + A) & 0x0ffffffff;
    H1 = (H1 + B) & 0x0ffffffff;
    H2 = (H2 + C) & 0x0ffffffff;
    H3 = (H3 + D) & 0x0ffffffff;
    H4 = (H4 + E) & 0x0ffffffff;
 
  }
 
  var temp = cvt_hex(H0) + cvt_hex(H1) + cvt_hex(H2) + cvt_hex(H3) + cvt_hex(H4);
 
  return temp.toLowerCase();
 
}

/**
*  MD5 (Message-Digest Algorithm)
**/
var MD5 = function (string) {
  function RotateLeft(lValue, iShiftBits) {
    return (lValue<<iShiftBits) | (lValue>>>(32-iShiftBits));
  }
  function AddUnsigned(lX,lY) {
    var lX4,lY4,lX8,lY8,lResult;
    lX8 = (lX & 0x80000000);
    lY8 = (lY & 0x80000000);
    lX4 = (lX & 0x40000000);
    lY4 = (lY & 0x40000000);
    lResult = (lX & 0x3FFFFFFF)+(lY & 0x3FFFFFFF);
    if (lX4 & lY4) { return (lResult ^ 0x80000000 ^ lX8 ^ lY8); }
    if (lX4 | lY4) {
      if (lResult & 0x40000000) { return (lResult ^ 0xC0000000 ^ lX8 ^ lY8);} 
      else { return (lResult ^ 0x40000000 ^ lX8 ^ lY8); }
    } else { return (lResult ^ lX8 ^ lY8); }
  }
  function F(x,y,z) { return (x & y) | ((~x) & z); }
  function G(x,y,z) { return (x & z) | (y & (~z)); }
  function H(x,y,z) { return (x ^ y ^ z); }
  function I(x,y,z) { return (y ^ (x | (~z))); }
  function FF(a,b,c,d,x,s,ac) {
    a = AddUnsigned(a, AddUnsigned(AddUnsigned(F(b, c, d), x), ac));
    return AddUnsigned(RotateLeft(a, s), b);
  };
  function GG(a,b,c,d,x,s,ac) {
    a = AddUnsigned(a, AddUnsigned(AddUnsigned(G(b, c, d), x), ac));
    return AddUnsigned(RotateLeft(a, s), b);
  };
  function HH(a,b,c,d,x,s,ac) {
    a = AddUnsigned(a, AddUnsigned(AddUnsigned(H(b, c, d), x), ac));
    return AddUnsigned(RotateLeft(a, s), b);
  };
  function II(a,b,c,d,x,s,ac) {
    a = AddUnsigned(a, AddUnsigned(AddUnsigned(I(b, c, d), x), ac));
    return AddUnsigned(RotateLeft(a, s), b);
  };
  function ConvertToWordArray(string) {
    var lWordCount;
    var lMessageLength = string.length;
    var lNumberOfWords_temp1=lMessageLength + 8;
    var lNumberOfWords_temp2=(lNumberOfWords_temp1-(lNumberOfWords_temp1 % 64))/64;
    var lNumberOfWords = (lNumberOfWords_temp2+1)*16;
    var lWordArray=Array(lNumberOfWords-1);
    var lBytePosition = 0;
    var lByteCount = 0;
    while ( lByteCount < lMessageLength ) {
      lWordCount = (lByteCount-(lByteCount % 4))/4;
      lBytePosition = (lByteCount % 4)*8;
      lWordArray[lWordCount] = (lWordArray[lWordCount] | (string.charCodeAt(lByteCount)<<lBytePosition));
      lByteCount++;
    }
    lWordCount = (lByteCount-(lByteCount % 4))/4;
    lBytePosition = (lByteCount % 4)*8;
    lWordArray[lWordCount] = lWordArray[lWordCount] | (0x80<<lBytePosition);
    lWordArray[lNumberOfWords-2] = lMessageLength<<3;
    lWordArray[lNumberOfWords-1] = lMessageLength>>>29;
    return lWordArray;
  };
  function WordToHex(lValue) {
    var WordToHexValue="",WordToHexValue_temp="",lByte,lCount;
    for (lCount = 0;lCount<=3;lCount++) {
      lByte = (lValue>>>(lCount*8)) & 255;
      WordToHexValue_temp = "0" + lByte.toString(16);
      WordToHexValue = WordToHexValue + WordToHexValue_temp.substr(WordToHexValue_temp.length-2,2);
    }
    return WordToHexValue;
  };
  function Utf8Encode(string) {
    string = string.replace(/\r\n/g,"\n");
    var utftext = "";
    for (var n = 0; n < string.length; n++) {
      var c = string.charCodeAt(n);
      if (c < 128) { utftext += String.fromCharCode(c); }
      else if((c > 127) && (c < 2048)) {
        utftext += String.fromCharCode((c >> 6) | 192);
        utftext += String.fromCharCode((c & 63) | 128);
      }
      else {
        utftext += String.fromCharCode((c >> 12) | 224);
        utftext += String.fromCharCode(((c >> 6) & 63) | 128);
        utftext += String.fromCharCode((c & 63) | 128);
      }
    }
    return utftext;
  };
  var x=Array();
  var k,AA,BB,CC,DD,a,b,c,d;
  var S11=7, S12=12, S13=17, S14=22; var S21=5, S22=9 , S23=14, S24=20;
  var S31=4, S32=11, S33=16, S34=23; var S41=6, S42=10, S43=15, S44=21;
  string = Utf8Encode(string); x = ConvertToWordArray(string);
  a = 0x67452301; b = 0xEFCDAB89; c = 0x98BADCFE; d = 0x10325476;
  for (k=0;k<x.length;k+=16) {
    AA=a; BB=b; CC=c; DD=d;
    a=FF(a,b,c,d,x[k+0], S11,0xD76AA478);
    d=FF(d,a,b,c,x[k+1], S12,0xE8C7B756);
    c=FF(c,d,a,b,x[k+2], S13,0x242070DB);
    b=FF(b,c,d,a,x[k+3], S14,0xC1BDCEEE);
    a=FF(a,b,c,d,x[k+4], S11,0xF57C0FAF);
    d=FF(d,a,b,c,x[k+5], S12,0x4787C62A);
    c=FF(c,d,a,b,x[k+6], S13,0xA8304613);
    b=FF(b,c,d,a,x[k+7], S14,0xFD469501);
    a=FF(a,b,c,d,x[k+8], S11,0x698098D8);
    d=FF(d,a,b,c,x[k+9], S12,0x8B44F7AF);
    c=FF(c,d,a,b,x[k+10],S13,0xFFFF5BB1);
    b=FF(b,c,d,a,x[k+11],S14,0x895CD7BE);
    a=FF(a,b,c,d,x[k+12],S11,0x6B901122);
    d=FF(d,a,b,c,x[k+13],S12,0xFD987193);
    c=FF(c,d,a,b,x[k+14],S13,0xA679438E);
    b=FF(b,c,d,a,x[k+15],S14,0x49B40821);
    a=GG(a,b,c,d,x[k+1], S21,0xF61E2562);
    d=GG(d,a,b,c,x[k+6], S22,0xC040B340);
    c=GG(c,d,a,b,x[k+11],S23,0x265E5A51);
    b=GG(b,c,d,a,x[k+0], S24,0xE9B6C7AA);
    a=GG(a,b,c,d,x[k+5], S21,0xD62F105D);
    d=GG(d,a,b,c,x[k+10],S22,0x2441453);
    c=GG(c,d,a,b,x[k+15],S23,0xD8A1E681);
    b=GG(b,c,d,a,x[k+4], S24,0xE7D3FBC8);
    a=GG(a,b,c,d,x[k+9], S21,0x21E1CDE6);
    d=GG(d,a,b,c,x[k+14],S22,0xC33707D6);
    c=GG(c,d,a,b,x[k+3], S23,0xF4D50D87);
    b=GG(b,c,d,a,x[k+8], S24,0x455A14ED);
    a=GG(a,b,c,d,x[k+13],S21,0xA9E3E905);
    d=GG(d,a,b,c,x[k+2], S22,0xFCEFA3F8);
    c=GG(c,d,a,b,x[k+7], S23,0x676F02D9);
    b=GG(b,c,d,a,x[k+12],S24,0x8D2A4C8A);
    a=HH(a,b,c,d,x[k+5], S31,0xFFFA3942);
    d=HH(d,a,b,c,x[k+8], S32,0x8771F681);
    c=HH(c,d,a,b,x[k+11],S33,0x6D9D6122);
    b=HH(b,c,d,a,x[k+14],S34,0xFDE5380C);
    a=HH(a,b,c,d,x[k+1], S31,0xA4BEEA44);
    d=HH(d,a,b,c,x[k+4], S32,0x4BDECFA9);
    c=HH(c,d,a,b,x[k+7], S33,0xF6BB4B60);
    b=HH(b,c,d,a,x[k+10],S34,0xBEBFBC70);
    a=HH(a,b,c,d,x[k+13],S31,0x289B7EC6);
    d=HH(d,a,b,c,x[k+0], S32,0xEAA127FA);
    c=HH(c,d,a,b,x[k+3], S33,0xD4EF3085);
    b=HH(b,c,d,a,x[k+6], S34,0x4881D05);
    a=HH(a,b,c,d,x[k+9], S31,0xD9D4D039);
    d=HH(d,a,b,c,x[k+12],S32,0xE6DB99E5);
    c=HH(c,d,a,b,x[k+15],S33,0x1FA27CF8);
    b=HH(b,c,d,a,x[k+2], S34,0xC4AC5665);
    a=II(a,b,c,d,x[k+0], S41,0xF4292244);
    d=II(d,a,b,c,x[k+7], S42,0x432AFF97);
    c=II(c,d,a,b,x[k+14],S43,0xAB9423A7);
    b=II(b,c,d,a,x[k+5], S44,0xFC93A039);
    a=II(a,b,c,d,x[k+12],S41,0x655B59C3);
    d=II(d,a,b,c,x[k+3], S42,0x8F0CCC92);
    c=II(c,d,a,b,x[k+10],S43,0xFFEFF47D);
    b=II(b,c,d,a,x[k+1], S44,0x85845DD1);
    a=II(a,b,c,d,x[k+8], S41,0x6FA87E4F);
    d=II(d,a,b,c,x[k+15],S42,0xFE2CE6E0);
    c=II(c,d,a,b,x[k+6], S43,0xA3014314);
    b=II(b,c,d,a,x[k+13],S44,0x4E0811A1);
    a=II(a,b,c,d,x[k+4], S41,0xF7537E82);
    d=II(d,a,b,c,x[k+11],S42,0xBD3AF235);
    c=II(c,d,a,b,x[k+2], S43,0x2AD7D2BB);
    b=II(b,c,d,a,x[k+9], S44,0xEB86D391);
    a=AddUnsigned(a,AA);
    b=AddUnsigned(b,BB);
    c=AddUnsigned(c,CC);
    d=AddUnsigned(d,DD);
  }
  var temp = WordToHex(a)+WordToHex(b)+WordToHex(c)+WordToHex(d);
  return temp.toLowerCase();
}

//64个基本的编码                                                                                            
var base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";                       
var base64DecodeChars = new Array(                                                                                
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,                                               
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,                                               
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63,                                               
    52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1,                                               
    -1,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14,                                               
    15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1,                                               
    -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,                                               
    41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1);                                              
//编码的方法                                                                                                      
function base64encode(str) {                                                                                      
    var out, i, len;                                                                                              
    var c1, c2, c3;                                                                                               
    len = str.length;                                                                                             
    i = 0;                                                                                                        
    out = "";                                                                                                     
    while(i < len) {                                                                                              
    c1 = str.charCodeAt(i++) & 0xff;                                                                              
    if(i == len)                                                                                                  
    {                                                                                                             
        out += base64EncodeChars.charAt(c1 >> 2);                                                                 
        out += base64EncodeChars.charAt((c1 & 0x3) << 4);                                                         
        out += "==";                                                                                              
        break;                                                                                                    
    }                                                                                                             
    c2 = str.charCodeAt(i++);                                                                                     
    if(i == len)                                                                                                  
    {                                                                                                             
        out += base64EncodeChars.charAt(c1 >> 2);                                                                 
        out += base64EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));                                   
        out += base64EncodeChars.charAt((c2 & 0xF) << 2);                                                         
        out += "=";                                                                                               
        break;                                                                                                    
    }                                                                                                             
    c3 = str.charCodeAt(i++);                                                                                     
    out += base64EncodeChars.charAt(c1 >> 2);                                                                     
    out += base64EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));                                       
    out += base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >>6));                                       
    out += base64EncodeChars.charAt(c3 & 0x3F);                                                                   
    }                                                                                                             
    return out;                                                                                                   
}                                                                                                                 
//解码的方法                                                                                                      
function base64decode(str) {                                                                                      
    var c1, c2, c3, c4;                                                                                           
    var i, len, out;                                                                                              
    len = str.length;                                                                                             
    i = 0;                                                                                                        
    out = "";                                                                                                     
    while(i < len) {                                                                                              
                                                                                                                  
    do {                                                                                                          
        c1 = base64DecodeChars[str.charCodeAt(i++) & 0xff];                                                       
    } while(i < len && c1 == -1);                                                                                 
    if(c1 == -1)                                                                                                  
        break;                                                                                                    
                                                                                                                  
    do {                                                                                                          
        c2 = base64DecodeChars[str.charCodeAt(i++) & 0xff];                                                       
    } while(i < len && c2 == -1);                                                                                 
    if(c2 == -1)                                                                                                  
        break;                                                                                                    
    out += String.fromCharCode((c1 << 2) | ((c2 & 0x30) >> 4));                                                   
                                                                                                                  
    do {                                                                                                          
        c3 = str.charCodeAt(i++) & 0xff;                                                                          
        if(c3 == 61)                                                                                              
        return out;                                                                                               
        c3 = base64DecodeChars[c3];                                                                               
    } while(i < len && c3 == -1);                                                                                 
    if(c3 == -1)                                                                                                  
        break;                                                                                                    
    out += String.fromCharCode(((c2 & 0XF) << 4) | ((c3 & 0x3C) >> 2));                                           
                                                                                                                  
    do {                                                                                                          
        c4 = str.charCodeAt(i++) & 0xff;                                                                          
        if(c4 == 61)                                                                                              
        return out;                                                                                               
        c4 = base64DecodeChars[c4];                                                                               
    } while(i < len && c4 == -1);                                                                                 
    if(c4 == -1)                                                                                                  
        break;                                                                                                    
    out += String.fromCharCode(((c3 & 0x03) << 6) | c4);                                                          
    }                                                                                                             
    return out;                                                                                                   
}                                                                                                                 

