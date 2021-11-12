$(document).ready(function(){
    $('a[data-toggle="pill"]').on('show.bs.tab', function(e) {
        localStorage.setItem('activeTab', $(e.target).attr('href'));
    });
    
    var activeTab = localStorage.getItem('activeTab');
    
    if(activeTab){
        $('#v-pills-tab a[href="' + activeTab + '"]').tab('show');
    }

    SetDateLimit();
});

function SetDateLimit(){
    var dtToday = new Date();

    var month = dtToday.getMonth() + 1;
    var day = dtToday.getDate();
    var year = dtToday.getFullYear();

    if(month < 10)
        month = '0' + month.toString();
    if(day < 10)
        day = '0' + day.toString();

    var maxDate = year + '-' + month + '-' + day;    
    $('#date_of_birth').attr('max', maxDate);
}


function CheckProfileName(){
    let profile_name = document.getElementById("profile_name");
    let profile_name_error = document.getElementById("profile_name_error");
    if (profile_name.value === ""){
        profile_name.classList.add("is-invalid");
        profile_name_error.innerHTML = "Name cannot be empty!";
        return false;
    }
    else{
        profile_name.classList.remove("is-invalid");
        profile_name_error.innerHTML = "";
        return true;
    }
}

function CheckDateOfBirth(){
    let date_of_birth = document.getElementById("date_of_birth");
    let date_of_birth_error = document.getElementById("date_of_birth_error");
    if (date_of_birth.value === ""){
        date_of_birth.classList.add("is-invalid");
        date_of_birth_error.innerHTML = "Please specify your date of birth!"
        return false;
    }
    else{
        date_of_birth.classList.remove("is-invalid");
        date_of_birth_error.innerHTML = "";
        return true;
    }
}

function UpdateProfileFormValidity(){
    return CheckProfileName() && CheckDateOfBirth();
}

// Change Email Form Checks
function CheckCurrentEmail(){
    let current_email = document.getElementById("current_email");
    let current_email_error = document.getElementById("current_email_error");
    if (current_email.value === ""){
        current_email.classList.add("is-invalid");
        current_email_error.innerHTML = "Current email cannot be empty!";
        return false;
    }
    else{
        if(CheckIfValidEmail(current_email.value)){
            current_email.classList.remove("is-invalid");
            current_email_error.innerHTML = "";
            return true;
        }
        else{
            current_email.classList.add("is-invalid");
            current_email_error.innerHTML = "Current email is not valid!";
            return false;
        }
    }
}

function CheckNewEmail(){
    let new_email = document.getElementById("new_email");
    let new_email_error = document.getElementById('new_email_error');
    if (new_email.value === ""){
        new_email.classList.add("is-invalid");
        new_email_error.innerHTML = "New email cannot be empty!";
        return false;
    }
    else{
        if(CheckIfValidEmail(new_email.value)){
            if (CheckNewEmailSimilar()){
                new_email.classList.add("is-invalid");
                new_email_error.innerHTML = "New email must be different from current email!";
                return false;
            }
            else{
                new_email.classList.remove("is-invalid");
                new_email_error.innerHTML = "";
                return true;
            }
        }
        else{
            new_email.classList.add("is-invalid");
            new_email_error.innerHTML = "Please enter a valid email!";
            return false;
        }
    }
}

function CheckIfValidEmail(data){
    return (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(data))
}

function CheckNewEmailSimilar(){
    let new_email = document.getElementById("new_email");
    let current_email = document.getElementById("current_email");
    return new_email.value === current_email.value;
}


function ChangeEmailFormValidity(){
    return CheckCurrentEmail() && CheckNewEmail();
}

// Change Password Form Checks
function CheckCurrentPassword(){
    let current_password = document.getElementById("current_password");
    let current_password_error = document.getElementById("current_password_error");
    if (current_password.value === ""){
        current_password.classList.add("is-invalid");
        current_password_error.innerHTML = "Password cannot be empty!";
        return false;
    }
    else{
        current_password.classList.remove("is-invalid");
        current_password_error.innerHTML = "";
        return true;
    }
}

function CheckNewPassword(){
    let new_password = document.getElementById("new_password");
    let new_password_error = document.getElementById('new_password_error');
    if (new_password.value === ""){
        new_password.classList.add("is-invalid");
        new_password_error.innerHTML = "New password cannot be empty!";
        return false;
    }
    else{
        if(/(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[A-z0-9?!@#$%^&*()]{8,}/.test(new_password.value)){
            new_password.classList.remove("is-invalid");
            new_password_error.innerHTML = "";
            return true;
        }
        else{
            new_password.classList.add("is-invalid");
            new_password_error.innerHTML = "Password must contain a minimum of eight characters, with at least one uppercase letter, one lowercase letter and one number. These are the allowable symbols: ?!@#$%^&*()";
            return false;
        }
    }
}

function CheckNewPassword2(){
    let new_password_2 = document.getElementById("new_password_2");
    let new_password_2_error = document.getElementById('new_password_2_error');
    if (new_password_2_error.value === ""){
        new_password_2.classList.add("is-invalid");
        new_password_2_error.innerHTML = "Field cannot be empty!";
        return false;
    }
    else{
        new_password_2.classList.remove("is-invalid");
        new_password_2_error.innerHTML = "";
        return true;
    }
}

function CheckNewPasswordSimilar(){
    let new_password = document.getElementById("new_password");
    let new_password_2 = document.getElementById("new_password_2");
    let new_password_error = document.getElementById('new_password_error');
    let new_password_2_error = document.getElementById('new_password_2_error');


    if (CheckNewPassword() && CheckNewPassword2()){
        if (new_password.value === new_password_2.value){
            new_password.classList.remove("is-invalid");
            new_password.classList.add("is-valid");
            new_password_2.classList.remove("is-invalid");
            new_password_2.classList.add("is-valid");
            new_password_2_error.innerHTML = "";
    
            return true;
        }
        else{
            new_password.classList.add("is-invalid");
            new_password_2.classList.add("is-invalid");
            new_password_2_error.innerHTML = "The password entered does not match the one above.";
            return false;
        }
    }
    else{
        return false;
    }
}

function ChangePasswordFormValidity(){
    return CheckNewPasswordSimilar() && CheckNewPassword() && CheckNewPassword2();
}