// bradley mackey
// web technology assignment 2018/19

var currentlyViewingMovie;

var ajax = {};
ajax.x = function () {
    if (typeof XMLHttpRequest !== 'undefined') {
        return new XMLHttpRequest();
    }
    var versions = [
        "MSXML2.XmlHttp.6.0",
        "MSXML2.XmlHttp.5.0",
        "MSXML2.XmlHttp.4.0",
        "MSXML2.XmlHttp.3.0",
        "MSXML2.XmlHttp.2.0",
        "Microsoft.XmlHttp"
    ];

    var xhr;
    for (var i = 0; i < versions.length; i++) {
        try {
            xhr = new ActiveXObject(versions[i]);
            break;
        } catch (e) {
        }
    }
    return xhr;
};

ajax.send = function (url, callback, method, data, async) {
    if (async === undefined) {
        async = true;
    }
    var x = ajax.x();
    x.open(method, url, async);
    x.onreadystatechange = function () {
        if (x.readyState == 4) {
            callback(x.responseText)
        }
    };
    if (method == 'POST') {
        x.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    }
    x.send(data)
};

ajax.get = function (url, data, callback, async) {
    var query = [];
    for (var key in data) {
        query.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]));
    }
    ajax.send(url + (query.length ? '?' + query.join('&') : ''), callback, 'GET', null, async)
};

ajax.post = function (url, data, callback, async) {
    var query = [];
    for (var key in data) {
        query.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]));
    }
    ajax.send(url, callback, 'POST', query.join('&'), async)
};

$(function() {

    // cookies -> user
    //         -> lang

    function updateUsernameDisplay() {
        var currentUsername = Cookies.get("user");
        var language = Cookies.get("lang");
        if (language === undefined) {
            language = "en";
        }
        if (currentUsername !== undefined) {
            $("#username-label").html(currentUsername);
            $("#login-button").removeClass("btn-success");
            $("#login-button").addClass("btn-danger");
            if (language === "en") {
                $("#login-button").html("Logout");
            } else {
                $("#login-button").html("Connectez - Out");
            }
        } else {
            $("#username-label").html("");
            $("#login-button").removeClass("btn-danger");
            $("#login-button").addClass("btn-success");
            if (language === "en") {
                $("#login-button").html("Login");
            } else {
                $("#login-button").html("S'identifier");
            }
        }
    }

    updateUsernameDisplay();

    function showLoginPage() {
        window.location.href = "/login";
    }

    function login(name) {
        if (name !== undefined && name !== null) {
            Cookies.set("user",name);
            window.location.href = "/";
        }
    }

    function logout() {
        Cookies.remove("user");
        window.location.href = "/login";
    }

    function changeLanguage(newLanguage) {
        Cookies.set("lang",newLanguage);
        location.reload();
    }

    function rateMovie(movie,rating) {

    }

    function errorNoUsername(shouldShow) {
        if (shouldShow) {
            $("#login-error-message").show();
        } else {
            $("#login-error-message").hide();
        } 
    }

    $("#toggle-login-form").submit(function(event) {
        event.preventDefault();
        var currentUser = Cookies.get("user");
        if (currentUser === undefined) {
            showLoginPage();
        } else {
            logout();
            showLoginPage();
        }
    });

    $("#login-form").submit(function(event) {
        event.preventDefault();
        var enteredUsername = $("#username-field").val().trim();
        if (enteredUsername === "" || enteredUsername === undefined || enteredUsername === null) {
            errorNoUsername(true);
            return;
        }
        errorNoUsername(false);
        login(enteredUsername);

        window.location.href = "/";

    });

    $("#username-field").change(function() {
        errorNoUsername(false);
    })


    $("#english-link").click(function() {
        changeLanguage("en");
    });

    $("#french-link").click(function() {
        changeLanguage("fr");
    });

    $('#rating-modal').on('shown.bs.modal', function () {
        console.log("modal focused!");
    });

    $(".card").click(function() {
        var currentUser = Cookies.get("user");
        if (currentUser === undefined) {
            showLoginPage();
            return;
        } else {
            currentlyViewingMovie = $(this).attr('id');
        }
    });


    $("#save-rating-button").click(function(event) {
        var currentUser = Cookies.get("user");
        if (currentUser === undefined) {
            showLoginPage();
            return;
        }
        $(".modal-footer").hide();
        $(".modal-title").hide();
        $(".rating-form").hide();
        $("#loader").show();
        var movieStarRating = $('input[name=stars]:checked').val();
        console.log(movieStarRating);
        console.log(currentlyViewingMovie);
        var url = "/review/"+currentlyViewingMovie;
        var payload = { 'user': currentUser, 'stars': movieStarRating };
        console.log(url);
        console.log(payload);

        ajax.post(url, payload, function() {
            console.log("all done!");
            window.location.reload();
        });
    });


});