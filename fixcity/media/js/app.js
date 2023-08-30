jQuery(document).ready(function ($) {
  $(document).superSelectify();

  // Quick extension for our AJAX voting widgets
  $.fn.voteify = function (options) {
    var defaults = {
      rackID: "1",
      activeClass: "rack-likes-active",
      targetChild: "strong"
    };
    var options = $.extend(defaults, options);
    return this.each(function () {
      obj = $(this);
      obj.bind("click", function (event) {
        var target = $(this);
        $.ajax({
          type: "POST",
          url: "/racks/" + options.rackID + "/votes/",
          dataType: "json",
          success: function (response) {
            target.children(options.targetChild).text(response.votes);
            if (target.is('.' + options.activeClass)) {
              target.removeClass(options.activeClass);
            } else {
              $('<span class="rack-likes ' + options.activeClass + '">' + target.html() + '</span>').insertBefore(target);
              target.remove();
            };
          }
        });
        return false;
      });
    });
  };

  $('.photo-guidelines').click(function () {
    Boxy.ask("<p class=\"content\">Photographs should show an unobstructed view of the suggested spot, curb, and storefront. Please copy these examples closely in terms of angle, zoom, and detail.</p><div class=\"selfclear\"><div class=\"leftwise\"<h2>Ideal</h2><img src=\"/site_media/img/rackphoto-ideal.jpg\" width=\"300\" height=\"201\" /></div><div class=\"rightwise\"><h2>Good</h2><img src=\"/site_media/img/rackphoto-good.jpg\" width=\"300\" height=\"201\"  /></div></div>", null, null, {
      title: "Photo Guidelines",
      closeable: true,
      contentClass: 'photos'
    });
    return false;
  });;
  $('.location-guidelines').click(function () {
    Boxy.ask("<div class=\"content selfclear\"><a class=\"rightwise\" href=\"/site_media/resources/PlacementGuide.pdf\"><img src=\"/site_media/img/rack_diagram-thumb.png\" width=\"160\" height=\"200\" /></a><p>Your location suggestion should comply with the requirements shown in this diagram. <a href=\"/site_media/resources/PlacementGuide.pdf\">Print</a> and take out with you to verify this location, or watch the <a href=\"http://www.streetfilms.org/archives/how-to-get-your-nyc-bike-racks/\">Rack Placement Streetfilm</a> to better inform your suggestions.</p></div>", null, null, {
      title: "Location Guidelines",
      closeable: true
    });
    return false;
  });

  $('<small> <a href="#">Photo Guidelines</a></small>').appendTo('label[for="fakebrowseinput"]').click(function () {
    Boxy.ask("<p class=\"content\">Photographs should show an unobstructed view of the suggested spot, curb, and storefront. Please copy these examples closely in terms of angle, zoom, and detail.</p><div class=\"selfclear\"><div class=\"leftwise\"<h2>Ideal</h2><img src=\"/site_media/img/rackphoto-ideal.jpg\" width=\"300\" height=\"201\" /></div><div class=\"rightwise\"><h2>Good</h2><img src=\"/site_media/img/rackphoto-good.jpg\" width=\"300\" height=\"201\"  /></div></div>", null, null, {
      title: "Photo Guidelines",
      closeable: true,
      contentClass: 'photos'
    });
    return false;
  });

  try {
    OpenLayers.ImgPath = "/site_media/img/mapicons/";
  } catch(err) {
    // no OpenLayers - we're probably on a static, mapless page
  }

  $('#content form .required').each(function () {
    var obj = $(this);
    if (obj.val() != '') {
      obj.removeClass('required')
    }
  }).bind("focus", function (event) {
    $(this).removeClass('required');
  }).bind("blur", function (event) {
    var obj = $(this);
    if (obj.val() == "") {
      obj.addClass('required');
    }
  }).bind("change", function (event) {
    var obj = $(this);
    if (obj.val() == "") {
      obj.addClass('required');
    }
  });

  $('#content form').addClass('expandable');
  $('#content form h2.toggler').click(function () {
    var target = $(this).next('.section');
    if (target.is(':hidden')) {
      $('#content form .section').slideUp("fast");
      $('#content form h2.toggler').removeClass('expanded');
      target.slideDown("fast");
      $(this).addClass('expanded');
    }
  });
  $('#content form h2.toggler:first').addClass('expanded').next('.section').show();

});

function expandOnce(selector, text) {
  var target = jQuery(selector);
  jQuery('<span class="expandonce">' + text + '</span>').prependTo(target).click(function () {
    jQuery(this).siblings().removeClass("noshow").end().remove();
  }).siblings().addClass("noshow");
}

jQuery.fn.infoSuffixify = function () { //chainable
  return this.each(function () {
    var obj = jQuery(this);
    jQuery('<img src="/site_media/img/info.png" alt="More information about this field" title="' + obj.attr('title') + '" />').click(function () {
      return false;
    }).appendTo('label[for="' + obj.attr('id') + '"]');
  });
};

// Taken from http://www.andrewpeace.com/textarea-maxlength.html
jQuery.fn.truncate = function (len) {
  this.val(this.val().substring(0, len));
  return false;
};

jQuery.fn.maxLength = function (len) {
  var maxLengthKeyPress = new Array();
  var maxLengthChange = new Array();
  var appleKeyOn = false;

  //the second argument should be true if len should be based on
  //the maxlength attribute instead of the input
  var useAttr = arguments.length > 1 ? arguments[1] : false;

  var handleKeyUp = function (e) {
    //if the apple key (macs) is being pressed, set the indicator
    if (e.keyCode == 224 || e.keyCode == 91) appleKeyOn = false;
  };

  var handleKeyDown = function (e) {
    //if the apple key (macs) is being released, turn off the indicator
    if (e.keyCode == 224 || e.keyCode == 91) appleKeyOn = true;
  };

  var handleKeyPress = function (e) {
    //if this keyCode does not increase the length of the textarea value,
    //just let it go
    if (appleKeyOn || (e.charCode == 0 && e.keyCode != 13) || e.ctrlKey) return;

    //get the textarea element
    var textarea = jQuery(this);
    //if the length should be based on the maxlength attribute instead of the
    //input, use that
    len = useAttr ? parseInt(textarea.attr('maxlength')) : len;
    //get the value of the textarea
    var val = textarea.val();
    //get the length of the current text selection
    var selected=0;
    try {
	    selected = Math.abs(textarea.attr('selectionStart') - textarea.attr('selectionEnd'));
	  } catch(err) {
	    // textArea not currently displayed or otherwise causing selection to fail
	  }
    selected = isNaN(selected) ? 0 : selected;
    //if this is the maximum length
    if (val.length == len && selected < 1) return false;
    else if (val.length > len && selected < (val.length - len)) return textarea.truncate(len);
  };

  var handleChange = function (e) {
    //get the textarea element
    var textarea = jQuery(this);

    //if the length should be based on the maxlength attribute instead of the
    //input, use that
    len = useAttr ? parseInt(textarea.attr('maxlength')) : len;

    //truncate the textarea to its proper length
    textarea.truncate(len);
  };

  //get the current keyup and change functions
  var removeKeyPress = maxLengthKeyPress[this.selector];
  var removeChange = maxLengthChange[this.selector];

  //remove the keyup and change functions from any matched elements in case
  //a maxlength was previously set and a new one is being set
  this.die('keypress', removeKeyPress);
  this.die('change', removeChange);

  if (len == 0 && !useAttr) return;

  //set the keyup and change functions for this element set and all future
  //elements matching this selector
  this.live('keypress', handleKeyPress);
  this.live('change', handleChange);
  this.live('keydown', handleKeyDown);
  this.live('keyup', handleKeyUp);

  //save the current keyup and change functions so that they can be
  //remove later
  maxLengthKeyPress[this.selector] = handleKeyPress;
  maxLengthChange[this.selector] = handleChange;

  //trigger a keypress event so that the limit will be enforced
  this.keypress();
};

var rack_icon_url = function(feature) {
  var n = feature.cluster.length;
  var all_pending = true;
  var all_verified = true;
  for (var i = 0; i < n; i++) {
    if (feature.cluster[i].attributes.status.value != 'pending') {
      all_pending = false;
    }
    if (feature.cluster[i].attributes.verified == null) {
      all_verified = false;
    }
  }
  if ( all_pending ) {
    return "/site_media/img/rack-pending-icon.png";
  } else if ( all_verified) {
    return "/site_media/img/rack-verified-icon.png";
  } else {
    return "/site_media/img/rack-icon.png";
  }
};

