$(document).ready(function(){
    $('a[data-toggle="pill"]').on('show.bs.tab', function(e) {
        localStorage.setItem('activeTab', $(e.target).attr('href'));
    });
    
    var activeTab = localStorage.getItem('activeTab');
    
    if(activeTab){
        $('#v-pills-tab a[href="' + activeTab + '"]').tab('show');
    }
});

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
        new_password.classList.remove("is-invalid");
        new_password_error.innerHTML = "";
        return true;
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
    return CheckNewPasswordSimilar();
}