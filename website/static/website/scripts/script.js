function toggleSpoiler(spoiler) {
	$(spoiler).parent(".spoiler").children(".spoiler_body").slideToggle("fast");
	return false;
}
function setCookieWithDocumentCookie(cookieName, value, expire_days) {
	var ExpireDate = new Date();
	ExpireDate.setTime(ExpireDate.getTime() + (expire_days * 24 * 3600 * 1000));
	document.cookie = cookieName + "=" + encodeURIComponent(value) +
		((expire_days == null) ? "" : "; expires=" + ExpireDate.toGMTString());
}

(function ($) {
	$.fn.textWidth = function () {
		var html_org = $(this).html();
		var html_calc = '<span>' + html_org + '</span>';
		$(this).html(html_calc);
		var width = $(this).find('span:first').width();
		$(this).html(html_org);
		return width;
	};
})(jQuery);

$(document).ready(function () {
	$("#bm_info_description_preview_audio").find("a").click(function () {
		return false;
	});
	$(".language_switch a").click(function () {
		if ($(this).attr("href") == 'switch-language-cn')
			setCookieWithDocumentCookie('lang', 'cn', 365);
		else
			setCookieWithDocumentCookie('lang', 'en', 365);
		location.reload();
		return false;
	});
	$(".listing_item").hover(
		function () {
			var that = $(this).find(".listing_item_title");
			var aw = that.width();
			var tw = that.textWidth();
			var delta = tw - aw;
			if (delta > 0) {
				function toLeft() {
					that.delay(1000).animate({textIndent: "-" + delta + "px"}, 2000, "swing", toRight);
				}

				function toRight() {
					that.delay(1000).animate({textIndent: "0px"}, 2000, "swing", toLeft);
				}

				toLeft();
			}
		},
		function () {
			var that = $(this).find(".listing_item_title");
			if (that.textIndent != 0)
				that.stop(true).animate({textIndent: "0px"}, "fast", "swing");
		}
	)
});
function fix_bm_img(image) {
	image.onerror = null;
	image.style.visibility = "hidden";
	function img_reload_callback() {
		image.style.visibility = "visible";
		return true;
	}

	image.onload = img_reload_callback;
	image.src = "https://s.ppy.sh/mt/" + (image.src.match(/\/([0-9]+)\.jpg/)[1]);
	return true;
}
function fix_bm_img_l(image) {
	image.onerror = null;
	image.style.visibility = "hidden";
	function img_reload_callback() {
		image.style.visibility = "visible";
		return true;
	}

	image.onload = img_reload_callback;
	image.src = "https://s.ppy.sh/mt/" + (image.src.match(/\/([0-9]+)\.jpg/)[1]) + 'l';
	return true;
}
function do_search(form) {
	if (!form.keyword.value)
		return false;
	var keyword = form.keyword.value;
	var c = encodeURIComponent(keyword);
	var uri = 'search.html?q=' + c;
	location.assign(uri);
	return false;
}