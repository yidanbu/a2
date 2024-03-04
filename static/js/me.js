document.addEventListener('DOMContentLoaded', function () {
    fetch('/me')
        .then(response => {
            if (response.ok) {
                return response.json()
            }else if (response.status === 403){
                alert("login failed, please check username and password")
                return ;
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            if (data.username) {
                // 在这里更新页面上的用户信息
                document.getElementById('user-info').textContent = 'User ID: ' + data.username;
                // hidden login/register button
                document.getElementById('login-link').style.display = 'none';
                document.getElementById('register-link').style.display = 'none';
            } else {
                // 处理用户未登录的情况
                document.getElementById('user-info').textContent = 'Please login to view your profile.';
                console.log(data.error);
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
});