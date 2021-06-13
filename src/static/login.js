/* Sign in with email and password using firebase. 
Display error messages if email or password are not filled out
or display error messages coming from FireBase. */

function SignInWithEmail() {
    var email = document.getElementById("inputEmail").value; //get email
    var password = document.getElementById("inputPassword").value; //get password
    if (email != "" && password != "") { //if both are filled out, then send to firebase for authentication
        firebase.auth().signInWithEmailAndPassword(email, password)
            .then((user) => {
                console.log(user);
                var ipaddress = '';
                $.ajax({
                    url: "https://api.ipify.org?format=json",
                    dataType: 'json',
                    async: false,
                    success: function(data) {
                        ipaddress = data.ip;
                        console.log(ipaddress + 'inside')
                    }
                });
                $.post('login', { email: email, ipaddress: ipaddress   },
                    function (response) {
                        window.location.href = 'dashboard#getStarted';
                    });

            })
            .catch((error) => {
                //console.log(error.message);
                $("#errorMessage").html(error.message);
                $("#errorMessage").show();
            });
    }

    else if (email == "") { //If email is empty
        $("#errorMessage").html("Please enter your email");
        $("#errorMessage").show();
    }
    else if (password == "") { //Otherwise, If password is empty
        $("#errorMessage").html("Please enter your password");
        $("#errorMessage").show();
    }

}

// Register with new email and password. Authentication happens via Firebase Authentication
function RegisterWithEmail() {
    var email = document.getElementById("registerEmail").value;
    var password = document.getElementById("registerPassword").value;
    var confirm_password = document.getElementById("registerConfirmPassword").value;
    if (email != "" && password != "" && password == confirm_password) { 
        //Checks if fields are filled and confirm_password matches password

        firebase.auth().createUserWithEmailAndPassword(email, password).then((user) => {
            console.log(user);
            $('#exampleModal').modal('hide');
            //Posts to login, where it can be stored as a session
            var ipaddress = '';
            $.ajax({
                url: "https://api.ipify.org?format=json",
                dataType: 'json',
                async: false,
                success: function(data) {
                    ipaddress = data.ip;
                    console.log(ipaddress + 'inside')
                }
            });
            $.post('login', { email: email, ipaddress: ipaddress  },
                function (response) {
                    window.location.href = 'dashboard#getStarted'; //Redirects to dashboard getting started page
                });
        }).catch(function (error) { //Display any error messages from Firebase
            $("#registerErrorMessage").html(error.message);
            $("#registerErrorMessage").show();
            console.log(error.message);
        });
    }
    else if (email == "") {
        $("#registerErrorMessage").html("Please enter your email");
        $("#registerErrorMessage").show();
    }
    else if (password == "") {
        $("#registerErrorMessage").html("Please enter your password!");
        $("#registerErrorMessage").show();
    }
    else if (password != confirm_password) {
        $("#registerErrorMessage").html("Passwords don't match");
        $("#registerErrorMessage").show();
    }
}

// Reset password. Users will need to enter the email id
// that was used to register and on clicking reset, an email will be sent
// to the user where they can click on a link and reset their password.
function ResetPassword() {
    var auth = firebase.auth();
    var emailAddress = document.getElementById("resetPasswordEmail").value;
    console.log(emailAddress)
    auth.sendPasswordResetEmail(emailAddress).then(function () {
        // Email sent.
        $("#resetPasswordSuccess").html("Email sent, please check your email for details.");
        $("#resetPasswordErrorMessage").hide();
        $("#resetPasswordSuccess").show();
    }).catch(function (error) {
        $("#resetPasswordErrorMessage").html(error.message);
        $("#resetPasswordSuccess").hide();
        $("#resetPasswordErrorMessage").show();
    });
}
// Sign-in with Google.
function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    var email = profile.getEmail();
    var ipaddress = '';
    $.ajax({
        url: "https://api.ipify.org?format=json",
        dataType: 'json',
        async: false,
        success: function(data) {
            ipaddress = data.ip;
            console.log(ipaddress + 'inside')
        }
      });
    $.post('login', { email: email, ipaddress: ipaddress  },
        function (response) {
            window.location.href = 'dashboard#getStarted';
        });
}

// Sign-in as a guest user
function signInAsGuest() {
    var email = 'Guest';
    var ipaddress = '';
    $.ajax({
        url: "https://api.ipify.org?format=json",
        dataType: 'json',
        async: false,
        success: function(data) {
            ipaddress = data.ip;
            console.log(ipaddress + 'inside')
        }
      });
    console.log(ipaddress + 'outside')
    $.post('login', { email: email, ipaddress: ipaddress },
        function (response) {
            window.location.href = 'dashboard#getStarted';
        });
}