// Code from Skye Fenton's CS50 Finance

let rform = document.querySelector("#register-form");

rform.onsubmit = function(event) {
    event.preventDefault();
    $.get("/check", {username: document.querySelector("#uname").value},
        function(data) {
            if (data) {
                rform.submit()
                return true;
            }
            else {
                alert("this username already exists");
                return false;
            }
        });
};