import { checkPassword } from './util.js';
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

    // check password meets requirements
    if (checkPassword(password) !== true) {
        alert('Password does not meet requirements. It must contains Upper and lower case letters, numbers and special characters @$!%*?& and be at least 8 characters long.');
        return;
    }

    // check email format
    if (!/\S+@\S+\.\S+/.test(email)) {
        alert('Invalid email format.');
        return;
    }

    // check username exists
    var data = {username: username};
    try {
        const response = await fetch('/username/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
        } else if (response.status === 409) {
            alert('username already exists');
            return;
        }
    } catch (error) {
        console.error('Error:', error);
        alert('check username failed due to technical reasons.');
        return;
    }

    // send register request
    var data = {
        username: username,
        password: password,
        first_name: first_name,
        last_name: last_name,
        address: address,
        email: email,
        phone: phone
    };

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert("register success")
            window.location.href = document.referrer;
        } else {
            alert('register failed. Please check your username and password.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Login failed due to technical reasons.');
    }
});
