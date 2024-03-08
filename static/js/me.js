document.addEventListener('DOMContentLoaded', function () {
    fetch('/me')
        .then(response => {
            const navbarContent = document.getElementById('navbarContent');
            if (response.ok) {
                // 用户已登录
                response.json().then(data => {
                    document.getElementById('general-info1').style.display = 'none';
                    document.getElementById('general-info2').style.display = 'none';
                    document.getElementById('navbarDropdown').innerHTML = data.username;
                    // get user role from data
                    // navbarContent.innerHTML = `
                    //     docu
                    // `;
                });
            } else {
                document.getElementById('navbarDropdown').style.display = 'none';
            }
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('login-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    // 获取用户输入的邮箱和密码
    var username = document.getElementById('login-username').value;
    var password = document.getElementById('login-password').value;

    // 构建请求体
    var data = {username: username, password: password};

    // 发送POST请求到Flask后端
    try {
        const response = await fetch('/login', {
            method: 'POST', // 或者 'GET' 如果你的后端是以查询字符串方式接收
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data) // 将JavaScript对象转换为JSON字符串
        });

        // 处理响应
        if (response.ok) {
            // 如果登录成功（即服务器返回的状态码是200）
            // 这里假设登录成功后服务器会重定向到主页
            localStorage.setItem("isLoggedIn", "true");
            window.location.reload()
        } else {
            // 如果登录失败（即服务器返回的状态码不是200）
            alert('Login failed. Please check your username and password.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Login failed due to technical reasons.');
    }

    // 登录成功，设置登录状态并重定向到主页面
    // window.location.href = '';
});