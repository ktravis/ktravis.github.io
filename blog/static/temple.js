// temple.js
// a micro-framework for AJAX template loading
// depends on jQuery and some specific html
//
// author : Kyle Travis
// license: MIT (ktravis.mit-license.org)

function loadContent(target) {
    if (!target) return;
    fixURL(target);
    $("#content-main").fadeOut(200, 
        function () { 
            var $el = $(this);
            $.ajax({
                url : target,
                data: { stub : true, },
            }).done(function (newContent) {
                $el.html(newContent);
                $el.fadeIn(300);
                pageCustoms(target);
                updateLinks();
            });
        });
}

function fixURL(newUrl) {
    window.location.hash = newUrl;
}
$(window).bind('hashchange', function (e) {
    var target = window.location.hash.split('#');
    target = target[target.length - 1];
    $el = $("#nav-set div").filter(function () {
        if (target == "") target = "/";
        return $(this).attr("href") == target;
    });
    if ($el.length > 0) doNavigate($el.attr("href"));
    else {
        console.log(target);
        loadContent(target);
    }
});

function pageCustoms(target) {}
function navCustoms(link) { 
var $el = $("#nav-set div").filter(function () {
            if (link && link.length > 1) {
                link = link.split("#");
                link = link[link.length - 1]
            } else link = "/";
            console.log(link + " " + $(this).attr("href"));
            return $(this).attr("href") == link;
    });
    return [$el.attr("title"), $el.attr("href")]; 
}

function doNavigate(href, noload) {
    if (!href) return;
    $(".active").removeClass("active");

    var a = navCustoms(href);
    title = a[0];
    href = a[1];

    if (!noload) loadContent(href);
}

function updateLinks() {
    $(".post-link").on("click", function(e) {
        loadContent($(this).attr("href"));
        e.preventDefault();
    });

    $(".back-link").on("click", function(e) {
        loadContent($(this).attr("href"));
        e.preventDefault();
    });
}

function setup() {
    $("#nav-set div").on("click", function () { 
            var href = $(this).attr('href');
            doNavigate(href);
            fixURL(href);
        });
    var x = window.location.hash;
    if (x) x = x.split("#");
    else x = "/";
    doNavigate(x[x.length - 1], false);
}