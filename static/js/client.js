$(function() {

    // cookies -> user
    //         -> lang

    function updateUsernameDisplay() {
        var currentUsername = Cookies.get("user");
        if (currentUsername !== undefined) {
            $("#username-label").html(currentUsername);
            $("#login-button").removeClass("btn-success");
            $("#login-button").addClass("btn-danger");
            $("#login-button").html("Logout");
        } else {
            $("#username-label").html("");
            $("#login-button").removeClass("btn-danger");
            $("#login-button").addClass("btn-success");
            $("#login-button").html("Login");
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
        updateUsernameDisplay();
    }

    function changeLanguage(newLanguage) {

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









});