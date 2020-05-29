function checkNameValidity(){
    let name = document.getElementById("name");
    let name_error = document.getElementById("name_error");
    if (name.value === ""){
        name_error.innerHTML = "Name cannot be empty!";
        name.className = "form-control is-invalid"
        return false
    }
    else{
        name_error.innerHTML = "";
        name.className = "form-control is-valid"
        return true
    }
}


function checkEmailValidity(){
    let email = document.getElementById("email");
    let email_error = document.getElementById("email_error")
    if (email.value === ""){
        email_error.innerHTML = "Email cannot be empty!";
        email.className = "form-control is-invalid";
        return false
    }
    else{
        if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email.value)){
            email_error.innerHTML = "";
            email.className = "form-control is-valid";
            return true
        }
        else{
            email_error.innerHTML = "Invalid email format!";
            email.className = "form-control is-invalid";
            return false
        }
    }
}


function checkPasswordValidity(){
    let password = document.getElementById("password");
    let password_error = document.getElementById("password_error");
    if (password.value === ""){
        password_error.innerHTML = "Password cannot be empty!";
        password.className = "form-control is-invalid";
        return false;
    }
    else{
        if(/(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[A-z0-9?!@#$%^&*()]{8,}/.test(password.value)){
            password_error.innerHTML = "";
            password.className = "form-control is-valid";
            return true;
        }
        else{
            password_error.innerHTML = "Password must contain a minimum of eight characters, with at least one uppercase letter, one lowercase letter and one number. These are the allowable symbols: ?!@#$%^&*()";
            password.className = "form-control is-invalid";
            return false;
        }
    }

}

function checkConfirmPasswordValidity(){
    let password = document.getElementById("password");
    let confirm_password = document.getElementById("password2");
    let confirm_password_error = document.getElementById("password2_error");
    if (confirm_password.value === password.value){
        confirm_password_error.innerHTML = "";
        confirm_password.className = "form-control is-valid";
        return true
    }
    else{
        confirm_password_error.innerHTML = "The password entered does not match the one above.";
        confirm_password.className = "form-control is-invalid";
        return false
    }
}

function registrationValidity(){
    return (checkNameValidity && checkEmailValidity() && checkPasswordValidity() && checkConfirmPasswordValidity())
}