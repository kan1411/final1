$(document).ready(function() {
    $('#registrationForm').submit(function(event) {
        event.preventDefault();

        var username = $('#username').val();
        var password = $('#password').val();
        var confirmPassword = $('#confirm-password').val();
        var name = $('#name').val();
        var gender = $('#gender').val();
        var role = $('#role').val();
        var area = $('#area').val();
        var phone = $('#phone').val();
        var academic = $('#academic').val();

        if (password !== confirmPassword) {
            $('#password-error').text('Mật khẩu không khớp!');
            return;
        }

        $.ajax({
            url: 'http://localhost:5000/checkUser', 
            method: 'POST',
            data: JSON.stringify({
                username: username,
                phone: phone
            }),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response) {
                $.ajax({
                    url: 'http://localhost:5000/register', 
                    method: 'POST',
                    data: JSON.stringify({
                        username: username,
                        password: password,
                        name: name,
                        gender: gender,
                        role: role,
                        area: area,
                        phone: phone,
                        academic: academic
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
                            localStorage.setItem('username', username);
                            localStorage.setItem('name', name); 
                            window.location.href = 'mainpage.html';
                        });
                    },
                    error: function(error) {
                        console.log(error);
                        alert('Đăng ký thất bại rồi lêu lêu!!!');
                    }
                });
            },
            error: function(error) {
                console.log(error);
                if (error.responseJSON && error.responseJSON.message) {
                    alert(error.responseJSON.message);
                } else {
                    alert('Kiểm tra username và phone thất bại!');
                }
            }
        });
    });
});

