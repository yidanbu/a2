// check register form validation
document.getElementById('registerForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // 阻止表单提交
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmPassword').value;
    var first_name = document.getElementById('first_name').value;
    var last_name = document.getElementById('last_name').value;
    var address = document.getElementById('address').value;
    var email = document.getElementById('email').value;
    var phone = document.getElementById('phone').value;

    // check if the password and confirmPassword match
    if (password !== confirmPassword) {
        alert('Passwords do not match.');
        return;
    }

    // 简单的邮箱格式校验
    if (!/\S+@\S+\.\S+/.test(email)) {
        alert('Invalid email format.');
        return;
    }

    // check username exists
    var data = {username: username};
    try {
        const response = await fetch('/username/check', {
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
        } else if (response.status === 409) {
            // 如果登录失败（即服务器返回的状态码不是200）
            alert('username already exists');
            return;
        }
    } catch (error) {
        console.error('Error:', error);
        alert('check username failed due to technical reasons.');
        return;
    }

    // send register request
     // 构建请求体
    var data = {
        username: username,
        password: password,
        first_name: first_name,
        last_name: last_name,
        address: address,
        email: email,
        phone: phone
    };

    // 发送POST请求到Flask后端
    try {
        const response = await fetch('/register', {
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
            alert("register success")
            window.location.href = '/'; // 重定向到主页
        } else {
            // 如果登录失败（即服务器返回的状态码不是200）
            alert('register failed. Please check your username and password.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Login failed due to technical reasons.');
    }
});
