document.getElementById('editProfileForm').addEventListener('submit', async function (event) {
    event.preventDefault();
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

    if (!/\S+@\S+\.\S+/.test(email)) {
        alert('Invalid email format.');
        return;
    }

    // send update request
    var data = {
        password: password,
        first_name: first_name,
        last_name: last_name,
        address: address,
        email: email,
        phone: phone
    };

    try {
        const response = await fetch(`/profile/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        // 处理响应
        if (response.ok) {
            alert("update profile success")
            window.location.reload();
        } else {
            alert('update profile failed. Please check your info.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('update profile failed due to technical reasons.');
    }
});
