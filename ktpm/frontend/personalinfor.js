$(document).ready(function() {
    var username = localStorage.getItem('username');
    var name = localStorage.getItem('name'); 

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

    // Chuyển hướng các nút
    $('#service-button').click(function() {
        window.location.href = 'service.html';
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

    $('#edit-profile-button').click(function() {
        $('#edit-username').val($('#username').text()).show();
        $('#edit-name').val($('#name').text()).show();
        $('#edit-gender').val($('#gender').text()).show();
        $('#edit-role').val($('#role').text()).show();
        $('#edit-area').val($('#area').text()).show();
        $('#edit-phone').val($('#phone').text()).show();
        $('#edit-academic').val($('#academic').text()).show();
        $('.edit-password').show();
        $('#save-profile-button').show();
    });

    $('#save-profile-button').click(function() {
        var formData = {
            username: $('#edit-username').val(),
            password: $('#edit-password').val(),
            confirm_password: $('#edit-confirm-password').val(),
            name: $('#edit-name').val(),
            gender: $('#edit-gender').val(),
            role: $('#edit-role').val(),
            area: $('#edit-area').val(),
            phone: $('#edit-phone').val(),
            academic: $('#edit-academic').val()
        };

        // Clear previous error messages
        $('.error-message').remove();

        $.ajax({
            type: 'POST',
            url: 'http://localhost:5000/update_userinfo',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            success: function(response) {
                if (response.error) {
                    if (response.error) {
                        $('#edit-phone');
                    } else {
                        Swal.fire({
                            icon: 'error',
                            title: 'Lỗi',
                            text: response.error,
                        });
                    }
                } else {
                    Swal.fire({
                        icon: 'success',
                        title: 'Thành công',
                        text: 'Cập nhật thông tin cá nhân thành công!',
                    }).then(() => {
                        location.reload();
                    });
                }
            },
            error: function(xhr, status, error) {
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    if (xhr.responseJSON.error) {
                        $('#edit-phone');
                    } else {
                        Swal.fire({
                            icon: 'error',
                            title: 'Lỗi',
                            text: xhr.responseJSON.error,
                        });
                    }
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi',
                        text: 'Đã xảy ra lỗi. Vui lòng thử lại.',
                    });
                }
            }
        });
    });

    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
        fetch(`http://localhost:5000/userinfo?username=${encodeURIComponent(storedUsername)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi',
                        text: data.error,
                    });
                } else {
                    $('#username').text(data.username);
                    $('#name').text(data.name);
                    $('#gender').text(data.gender);
                    $('#role').text(data.role);
                    $('#area').text(data.area);
                    $('#phone').text(data.phone);
                    $('#academic').text(data.academic);
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Lỗi',
                    text: 'Đã xảy ra lỗi. Vui lòng thử lại.',
                });
            });
    }
});
