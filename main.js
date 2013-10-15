
var rot = {amt: 20};
var points = { "projects" : 20,
               "blog" : 0,
               "about" : -20 };

var sections = {
"projects" :'<div class="content-body" id="projects">'
        +   '   <h1>Projects</h1>'
        +   '   <hr>'
        +   '   <p><a href="//www.kongregate.com/games/kmakai/isolation">ISOLATION</a> ( a game about personal space )</p>'
        +   '   <p><a href="//ktravis.github.io/yt-freedom">YOUTUBE FREEDOM</a> ( minimalist viewing window for youtube )</p>'
        +   '   <p><a href="//tinyforum.herokuapp.com">TINYFORUM</a> ( a small bulletin board system, written in clojure )</p>'
        +   '   <p>HUSK ( interactive fiction game and platform )</p>'
        +   '   <p><a href="//gist.github.com/ktravis">SCRAPS</a> ( minor works... )</p>'
        +   '</div>',

"blog" :    '<div class="content-body" id="blog">'
        +   '   <h1>Blog</h1>'
        +   '   <hr>'
        +   '   <p>coming soon...</p>'
        +   '</div>',

"about" :   '<div class="content-body" id="about">'
        +   '   <h1>About</h1>'
        +   '   <hr>'
        +   '   <p><pre>ktravis = {\n\t"name"       : "Kyle Travis",\n\t"location"   : "Eugene, OR",\n\t"occupation" : "Student",\n\t"studying"   : ("Math", "Physics"),\n\t"email"      : "<a href="mailto:ktravis@uoregon.edu">ktravis@uoregon.edu</a>",\n\t"twitter"    : "<a href="//www.twitter.com/kmakai">@kmakai</a>",\n\t"github"     : "<a href="//github.com/ktravis">github://ktravis</a>"\n}</pre></p>'
        +   '   <div id="about-more"> . . . </div>'
        +   '   <div id="about-hidden">Kyle Travis is a student of Applied Math and Physics at the University of Oregon, where he works part-time as a research assistant creating analysis software. Kyle develops small <a href="//kongregate.com/accounts/kmakai">games</a> and web applications when not arguing with compilers or scanning javadocs. <br><br>Languages and tools of choice:<ul><li>python</li><li>java</li><li>javascript</li><li>clojure</li><li>openGL</li><li>vim</li><li>archlinux</li><li>github</li></ul></div>'
        +   '</div>'};

function update() { 
    $("#nav-set").css({
        "-webkit-transform": "rotate(" + rot.amt + "deg)",
        "-moz-transform": "rotate(" + rot.amt + "deg)",
        "transform": "rotate(" + rot.amt + "deg)",
        "zoom": 1
    });
}

function rotate(deg) {
    $(rot).animate({amt: deg}, {
        duration: 1000,
        step: update,
        easing: "easeInOutCubic"
    });
}

function rotateTo(target) {
    rotate(points[target]);
}

function loadContent(target) {
    $("#content-main").fadeOut(200, 
            function () { 
                $(this).html(sections[target]);
                $(this).fadeIn(300);
                if (target == "about") {
                    $("#about-more").on("click", function() {
                            $(this).slideUp(800);
                            $("#about-hidden").slideDown(800);
                    });
                }
            });
}

$(document).ready(function () {
    $("#nav-set div").on("click", function () { 
            var title = $(this).attr("title");
            $(".active").removeClass("active");
            rotateTo(title);
            $(this).addClass("active"); 

            loadContent(title);
        });
    $("#s1").click();
});
