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
    });
    $('#personalinfor-button').click(function() {
        window.location.href = 'personalinfor.html';
    });
    $('#classform-button').click(function() {
        window.location.href = 'classform.html';
    });
    $('#searching-button').click(function() {
        window.location.href = 'search.html';
    });
    $('#mainpage-button').click(function() {
        window.location.href = 'mainpage.html';
    });
    $('#classinfor-button').click(function() {
        window.location.href = 'classinfor.html';
    });

    console.log('Username in mainpage:', username);
    console.log('Name in mainpage:', name);
});

$('#searchingform').submit(function(event) {
    event.preventDefault();

    var object = $('#object').val();
    var subject = $('#subject').val();
    var grade = $('#grade').val();
    var gender = $('#gender').val();
    var area = $('#area').val();
    var cond = $('#cond').val() || '';
    var academic = $('#academic').val();
    var username = localStorage.getItem('username');

    if (!object || !subject || !grade || !gender || !area || !academic) {
        Swal.fire({
            title: 'Lỗi!',
            text: 'Vui lòng điền đầy đủ thông tin vào tất cả các trường.',
            icon: 'error'
        });
        return;
    }

    console.log({
        object: object,
        subject: subject,
        grade: grade,
        gender: gender,
        area: area,
        cond: cond,
        academic: academic,
        username: username
    });

    $.ajax({
        url: 'http://localhost:5000/classform',
        method: 'POST',
        data: JSON.stringify({
            object: object,
            subject: subject,
            grade: grade,
            gender: gender,
            area: area,
            cond: cond,
            academic: academic,
            username: username
        }),
        contentType: 'application/json',
        dataType: 'json',
        success: function(response) {
            Swal.fire({
                title: 'Thành công!',
                text: response.message,
                icon: 'success',
                timer: 2000,
                showConfirmButton: false
            }).then(() => {
                window.location.href = 'search.html';
            });
        },
        error: function(error) {
            console.log(error);
            Swal.fire({
                title: 'Lỗi!',
                text: 'Đã xảy ra lỗi. Vui lòng thử lại.',
                icon: 'error'
            });
        }
    });
});
