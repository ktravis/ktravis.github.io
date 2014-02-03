var rot = {amt: 20};
var points = { "projects" : 20,
               "blog" : 0,
               "about" : -20 };

function update() { 
    $("#nav-set").css({
        "-webkit-transform": "rotate(" + rot.amt + "deg)",
        "-moz-transform": "rotate(" + rot.amt + "deg)",
        "transform": "rotate(" + rot.amt + "deg)",
        "zoom": 1
    });
}

function rotate(deg, callback) {
    $(rot).animate({amt: deg}, {
        duration: 1000,
        step: update,
        easing: "easeInOutCubic",
        complete: callback,
    });
}

function rotateTo(target, callback) {
    rotate(points[target], callback);
}

function pageCustoms(target) {
    if (target.match("about")) {
        $("#about-more").on("click", function() {
            $(this).slideUp(800);
            $("#about-hidden").slideDown(800);
        });
    }
}

function navCustoms(link) {
    if (link && link.length > 1) {
        link = link.split("#");
        link = link[link.length - 1]
    } else link = "/";
    if (link.match("/post")) {
        title = "blog";
        p = "/blog";
    } else p = link;
    var $el = $("#nav-set div").filter(function () {
            return $(this).attr("href") == p;
    });
    var title = $el.attr("title");
    rotateTo(title);
    $el.addClass("active"); 
    return [title, link]; 
}

$(document).ready(function () {
    setup();
});