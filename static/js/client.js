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

        }
    });



});