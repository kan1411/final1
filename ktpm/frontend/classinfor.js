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

    // Load my classes
    function loadMyClasses() {
        $.ajax({
            url: 'http://127.0.0.1:5000/my_classes',
            method: 'GET',
            data: { username: username },
            dataType: 'json',
            success: function(data) {
                const container = $('#MyClasses');
                container.empty(); 
                if (data.error) {
                    container.html(`<p>Lỗi: ${data.error}</p>`);
                } else if (data.length === 0) {
                    container.html('<p>Không có dữ liệu để hiển thị.</p>');
                } else {
                    data.forEach(cls => {
                        const card = $(`
                            <div class="class-card">
                                <p>Vai trò: ${cls.object}</p>
                                <p>Môn học: ${cls.subject}</p>
                                <p>Khối: ${cls.grade}</p>
                                <p>Giới tính: ${cls.gender}</p>
                                <p>Khu vực: ${cls.area}</p>
                                <p>Điều kiện khác: ${cls.cond}</p>
                                <p>Trạng thái: ${cls.approved === 1 ? 'Đã được duyệt' : 'Chưa được duyệt'}</p>
                                <p>Người đăng ký: ${cls.registered_by ? `<a href="#" class="user-link" data-username="${cls.registered_by}" data-class-id="${cls.id}">${cls.registered_by}</a>` : 'Chưa có người đăng ký'}</p>
                                <div class="user-info" style="display: none;"></div>
                            </div>
                        `);
                        container.append(card);
                    });
                }
            },
            error: function(xhr, status, error) {
                $('#MyClasses').html(`<p>Lỗi khi lấy dữ liệu: ${xhr.statusText}</p>`);
            }
        });
    }

    function loadRegisteredClasses() {
        $.ajax({
            url: 'http://127.0.0.1:5000/registered_classes',
            method: 'GET',
            data: { username: username },
            dataType: 'json',
            success: function(data) {
                const container = $('#RegisteredClasses');
                container.empty();
                if (data.error) {
                    container.html(`<p>Lỗi: ${data.error}</p>`);
                } else if (data.length === 0) {
                    container.html('<p>Không có dữ liệu để hiển thị.</p>');
                } else {
                    data.forEach(cls => {
                        const card = $(`
                            <div class="class-card">
                                <p>Vai trò: ${cls.object}</p>
                                <p>Môn học: ${cls.subject}</p>
                                <p>Khối: ${cls.grade}</p>
                                <p>Giới tính: ${cls.gender}</p>
                                <p>Khu vực: ${cls.area}</p>
                                <p>Điều kiện khác: ${cls.cond}</p>
                                <p>Trạng thái: ${cls.approved === 1 ? 'Đã được duyệt' : 'Chưa được duyệt'}</p>
                                <p>Tình trạng nhận lớp: ${cls.status}</p>
                            </div>
                        `);
                        container.append(card);
                    });
                }
            },
            error: function(xhr, status, error) {
                $('#RegisteredClasses').html(`<p>Lỗi khi lấy dữ liệu: ${xhr.statusText}</p>`);
            }
        });
    }

    $('#myClasses-tab').click(function() {
        loadMyClasses();
    });

    $('#registeredClasses-tab').click(function() {
        loadRegisteredClasses();
    });

    // Load my classes on page load
    loadMyClasses();

    // Handle user link click
    $(document).on('click', '.user-link', function(event) {
        event.preventDefault();
        const username = $(this).data('username');
        const classId = $(this).data('class-id');
        const userInfoContainer = $(this).closest('.class-card').find('.user-info');
        
        $.ajax({
            url: 'http://127.0.0.1:5000/get_user_info',
            method: 'GET',
            data: { username: username },
            dataType: 'json',
            success: function(data) {
                if (data.error) {
                    userInfoContainer.html(`<p>Lỗi khi lấy dữ liệu người dùng: ${data.error}</p>`);
                } else {
                    userInfoContainer.html(`
                        <p>Tên: ${data.name}</p>
                        <p>Giới tính: ${data.gender}</p>
                        <p>Khu vực: ${data.area}</p>
                        <p>Số điện thoại: ${data.phone}</p>
                        <p>Trình độ học vấn: ${data.academic}</p>
                        <button class="accept-class btn btn-primary" data-class-id="${classId}">Nhận</button>
                    `);
                    userInfoContainer.slideToggle();
                }
            },
            error: function(xhr, status, error) {
                userInfoContainer.html(`<p>Lỗi khi lấy dữ liệu: ${xhr.statusText}</p>`);
                userInfoContainer.slideToggle();
            }
        });
    });

    // Handle accept class click
    $(document).on('click', '.accept-class', function(event) {
        event.preventDefault();
        const classId = $(this).data('class-id');
        
        $.ajax({
            url: 'http://127.0.0.1:5000/accept_registration',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ class_id: classId }),
            success: function(response) {
                Swal.fire({
                    title: 'Nhận lớp thành công!',
                    icon: 'success',
                    timer: 2000,
                    showConfirmButton: false
                }).then(() => {
                    location.reload();
                });
            },
            error: function(xhr, status, error) {
                Swal.fire({
                    title: 'Lỗi!',
                    text: 'Đã xảy ra lỗi khi nhận lớp. Vui lòng thử lại.',
                    icon: 'error'
                });
            }
        });
    });
});

