$(document).ready(function() {
    var name = localStorage.getItem('name');
    var username = localStorage.getItem('username');

    if (name && username) {
        $('#username-display').text(name);
        $('#userDropdown').show();
        $('#loginSignup').hide();
    } else {
        $('#userDropdown').hide();
        $('#loginSignup').show();
    }

    $('#logout-button').click(function() {
        localStorage.removeItem('username');
        localStorage.removeItem('name');
        window.location.href = 'login.html'; 
    });
    $('#service-button').click(function() {
        window.location.href = 'service.html';
    })
    $('#personalinfor-button').click(function() {
        window.location.href = 'personalinfor.html';
    })
    $('#classform-button').click(function() {
        window.location.href = 'classform.html';
    })
    $('#searching-button').click(function() {
        window.location.href = 'search.html';
    })
    $('#mainpage-button').click(function() {
        window.location.href = 'mainpage.html';
    })
    $('#classinfor-button').click(function() {
        window.location.href = 'classinfor.html';
    })

    console.log('Username in mainpage:', username);
    console.log('Name in mainpage:', name);
});