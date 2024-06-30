$(document).ready(function() {
    $('#loginForm').submit(function(event) {
        event.preventDefault();
  
        var username = $('#username').val();
        var password = $('#password').val();
  
        console.log('Submitting form with:', username, password);
  
        $.ajax({
            url: 'http://localhost:5000/login', 
            method: 'POST',
            data: JSON.stringify({
                username: username,
                password: password
            }),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response) {
                console.log('Response from server:', response)
                console.log('Response keys:', Object.keys(response)); 
                
                if (response.username && response.name) { 
                    console.log('Saving to localStorage:', response.username, response.name);
                    localStorage.setItem('username', response.username);
                    localStorage.setItem('name', response.name);
                    
                    Swal.fire({
                        title: 'Thành công!',
                        text: response.message,
                        icon: 'success',
                        timer: 2000,
                        showConfirmButton: false
                    }).then(() => {
                        window.location.href = 'mainpage.html'; 
                    });
                } else {
                    console.error('Phản hồi không chứa username hoặc name');
                }
            },
            error: function(error) {
                console.log('Error from server:', error);
                Swal.fire({
                    title: 'Lỗi!',
                    text: 'Tài khoản hoặc mật khẩu lỗi',
                    icon: 'error'
                });
            }
        });
    });
  
    var username = localStorage.getItem('username');
    console.log('Username in localStorage:', username);
    if (username) {
        $('#userDropdown').text(username);
    }
});
