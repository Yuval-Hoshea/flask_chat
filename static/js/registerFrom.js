const goodMsg = "<b>Good password and username.</b>";
const badMsg = "<b>Please follow the rules</b>";


function checkValidForm(){
    let username = document.getElementById("username").value;
    let pass1 = document.getElementById("password").value;
    let pass2 = document.getElementById("re-password").value;
    //console.log(username, pass1, pass2);

    if (username.length > 20 || username.length < 3)
        return false;
    if (pass1.length < 8 || pass1.length > 20 )
        return false;
    if (pass1 != pass2)
        return false;
    //at least 1 upper letter, 1 lower letter, 1 digit
    return RegExp("(?=.*\\d.*)(?=.*[a-z].*)(?=.*[A-Z].*)").test(pass1);
}


function validForm(){
    let valid = checkValidForm();
    let textBox = document.getElementById("valid");
    
    if (valid)
        textBox.innerHTML = goodMsg;
    else
        textBox.innerHTML = badMsg;

    return valid;
}


function toLogin(){
    const url = document.getElementById("url").innerText;
    let mainForm = document.getElementById("registerForm");
    mainForm.method = "GET";
    mainForm.action = url;
    mainForm.submit();

    return true;
}