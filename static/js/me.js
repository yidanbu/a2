document.addEventListener('DOMContentLoaded', function () {
    fetch('/me')
        .then(response => {
            const navbarContent = document.getElementById('navbarContent');
            if (response.ok) {
                response.json().then(data => {
                    document.getElementById('general-info1').style.display = 'none';
                    document.getElementById('general-info2').style.display = 'none';
                    document.getElementById('navbarDropdown').innerHTML = data.username;
                });
            } else {
                document.getElementById('navbarDropdown').style.display = 'none';
            }
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('login-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    var username = document.getElementById('login-username').value;
    var password = document.getElementById('login-password').value;

    var data = {username: username, password: password};

    try {
        const response = await fetch('/login', {
            method: 'POST', // 或者 'GET' 如果你的后端是以查询字符串方式接收
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data) // 将JavaScript对象转换为JSON字符串
        });

        if (response.ok) {
            localStorage.setItem("isLoggedIn", "true");
            window.location.reload()
        } else {
            alert('Login failed. Please check your username and password.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Login failed due to technical reasons.');
    }
});