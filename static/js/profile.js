document.getElementById('editProfileForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // 阻止表单提交
    var id = document.getElementById('id').value;
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirm-password').value;
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

    // send update request
    // 构建请求体
    var data = {
        password: password,
        first_name: first_name,
        last_name: last_name,
        address: address,
        email: email,
        phone: phone
    };

    // 发送POST请求到Flask后端
    try {
        const response = await fetch(`/profile/${id}`, {
            method: 'PUT', // 或者 'GET' 如果你的后端是以查询字符串方式接收
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data) // 将JavaScript对象转换为JSON字符串
        });

        // 处理响应
        if (response.ok) {
            // 如果登录成功（即服务器返回的状态码是200）
            // 这里假设登录成功后服务器会重定向到主页
            alert("update profile success")
            window.location.reload();
        } else {
            // 如果登录失败（即服务器返回的状态码不是200）
            alert('update profile failed. Please check your info.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('update profile failed due to technical reasons.');
    }
});
