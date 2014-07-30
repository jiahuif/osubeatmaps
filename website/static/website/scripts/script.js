function toggleSpoiler(spoiler) {
    $(spoiler).parent(".spoiler").children(".spoiler_body").slideToggle("fast");
    return false;
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
    );
    /* disable lazy-load feature of official osu! website. */
    $("img.lazy-load").attr('src', function () {
        return $(this).data().src;
    });
});

function do_search(form) {
    if (!form.keyword.value)
        return false;
    var keyword = form.keyword.value;
    var c = encodeURIComponent(keyword);
    var uri = 'search.html?q=' + c;
    location.assign(uri);
    return false;
}

function redirect_to(url) {
    location.href = url;
}

function renderProxyDownloadServer(server) {
    var root = $("#bm_download_list").find("ul");
    var sourceElement = root.find("li").eq(server.sourceIndex);
    var sourceUrl = sourceElement.find('a').attr('href');
    var destinationUrl = sourceUrl.replace(server.regex, server.replace);
    var destinationElement = sourceElement.clone();
    destinationElement.find('a').attr('href', destinationUrl);
    destinationElement.find(".mirror_link").html(
            server.name + '<span class="country">' + server.location + '</span>'
    );
    root.append(destinationElement)

}
