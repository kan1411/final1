$(document).ready(function() {
    var username = localStorage.getItem('username');
    if (!username) {
        $('#loginMessage').show();
    } else {
        $('#admin').show();
        $('#logoutBtn').click(function() {
            localStorage.removeItem('username');
            window.location.href = 'adlogin.html';
        });

        function loadUsers() {
            console.log('Loading users...');
            $.ajax({
                url: 'http://localhost:5000/users',
                method: 'GET',
                dataType: 'json',
                success: function(users) {
                    console.log('Users loaded:', users);
                    var usersTableBody = $('#usersTable tbody');
                    usersTableBody.empty();
                    users.forEach(function(user) {
                        var row = `<tr>
                            <td>${user.id}</td>
                            <td>${user.username}</td>
                            <td>${user.name}</td>
                            <td>${user.gender}</td>
                            <td>${user.role}</td>
                            <td>${user.area}</td>
                            <td>${user.phone}</td>
                            <td>${user.academic}</td>
                            <td><button class="btn btn-danger deleteUserBtn" data-id="${user.id}">Xóa</button></td>
                        </tr>`;
                        usersTableBody.append(row);
                    });
                },
                error: function(error) {
                    console.log('Error loading users:', error);
                    Swal.fire({
                        title: 'Lỗi!',
                        text: 'Lỗi khi lấy danh sách người dùng',
                        icon: 'error'
                    });
                }
            });
        }

        function loadClassForms() {
            console.log('Loading class forms...');
            $.ajax({
                url: 'http://localhost:5000/forms',
                method: 'GET',
                dataType: 'json',
                success: function(forms) {
                    console.log('Class forms loaded:', forms);
                    var formsTableBody = $('#classFormsTable tbody');
                    formsTableBody.empty();
                    forms.forEach(function(form) {
                        var row = `<tr>
                            <td>${form.id}</td>
                            <td>${form.object}</td>
                            <td>${form.subject}</td>
                            <td>${form.grade}</td>
                            <td>${form.gender}</td>
                            <td>${form.area}</td>
                            <td>${form.cond}</td>
                            <td>
                                <button class="btn btn-success approveFormBtn" data-id="${form.id}">Duyệt</button>
                                <button class="btn btn-danger deleteFormBtn" data-id="${form.id}">Xóa</button>
                            </td>
                        </tr>`;
                        formsTableBody.append(row);
                    });
                },
                error: function(error) {
                    console.log('Error loading class forms:', error);
                    Swal.fire({
                        title: 'Lỗi!',
                        text: 'Lỗi khi lấy danh sách form tạo lớp',
                        icon: 'error'
                    });
                }
            });
        }

        $('body').on('click', '.deleteUserBtn', function() {
            var userId = $(this).data('id');
            console.log('Deleting user with ID:', userId);
            $.ajax({
                url: `http://localhost:5000/users/${userId}`,
                method: 'DELETE',
                success: function(response) {
                    console.log('User deleted:', response);
                    Swal.fire({
                        title: 'Thành công!',
                        text: response.message,
                        icon: 'success'
                    }).then(() => {
                        loadUsers();
                    });
                },
                error: function(error) {
                    console.log('Error deleting user:', error);
                    Swal.fire({
                        title: 'Lỗi!',
                        text: 'Lỗi khi xóa người dùng',
                        icon: 'error'
                    });
                }
            });
        });

        $('body').on('click', '.approveFormBtn', function() {
            var formId = $(this).data('id');
            console.log('Approving form with ID:', formId);
            $.ajax({
                url: `http://localhost:5000/forms/${formId}/approve`,
                method: 'POST',
                success: function(response) {
                    console.log('Form approved:', response);
                    Swal.fire({
                        title: 'Thành công!',
                        text: response.message,
                        icon: 'success'
                    }).then(() => {
                        loadClassForms();
                    });
                },
                error: function(error) {
                    console.log('Error approving form:', error);
                    Swal.fire({
                        title: 'Lỗi!',
                        text: 'Lỗi khi duyệt form',
                        icon: 'error'
                    });
                }
            });
        });

        $('body').on('click', '.deleteFormBtn', function() {
            var formId = $(this).data('id');
            console.log('Deleting form with ID:', formId);
            $.ajax({
                url: `http://localhost:5000/forms/${formId}`,
                method: 'DELETE',
                success: function(response) {
                    console.log('Form deleted:', response);
                    Swal.fire({
                        title: 'Thành công!',
                        text: response.message,
                        icon: 'success'
                    }).then(() => {
                        loadClassForms();
                    });
                },
                error: function(error) {
                    console.log('Error deleting form:', error);
                    Swal.fire({
                        title: 'Lỗi!',
                        text: 'Lỗi khi xóa form',
                        icon: 'error'
                    });
                }
            });
        });

        loadUsers();
        loadClassForms();
    }
});
