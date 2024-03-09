// document.getElementById('login-form').addEventListener('submit', async function (e) {
//     e.preventDefault();
//     // 获取用户输入的邮箱和密码
//     var username = document.getElementById('login-username').value;
//     var password = document.getElementById('login-password').value;
//
//     // 构建请求体
//     var data = {username: username, password: password};
//
//     // 发送POST请求到Flask后端
//     try {
//         const response = await fetch('/login', {
//             method: 'POST', // 或者 'GET' 如果你的后端是以查询字符串方式接收
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify(data) // 将JavaScript对象转换为JSON字符串
//         });
//
//         // 处理响应
//         if (response.ok) {
//             // 如果登录成功（即服务器返回的状态码是200）
//             // 这里假设登录成功后服务器会重定向到主页
//             localStorage.setItem("isLoggedIn", "true");
//             window.location.reload()
//         } else {
//             // 如果登录失败（即服务器返回的状态码不是200）
//             alert('Login failed. Please check your username and password.');
//         }
//     } catch (error) {
//         console.error('Error:', error);
//         alert('Login failed due to technical reasons.');
//     }
//
//     // 登录成功，设置登录状态并重定向到主页面
//     // window.location.href = '';
// });
// document.addEventListener('DOMContentLoaded', function () {
//     const buttons = document.querySelectorAll(".image-action");
//     buttons.forEach(button => {
//         button.addEventListener('click', async function (e) {
//             e.preventDefault();
//
//             const buttonInfo = button.getAttribute("name");
//             const fields = buttonInfo.split("-");
//             if (fields[0] !== "image") {
//                 return;
//             }
//             const imageId = fields[1];
//             const action = fields[2];
//             if (action === "setprimary") {
//                 try {
//                     const response = await fetch(`${window.location.href}/image/${imageId}/primary`, {
//                         method: 'PUT',
//                         headers: {
//                             'Content-Type': 'application/json',
//                         }
//                     });
//                     if (response.ok) {
//                         alert("set primary image success");
//                         window.location.reload();
//                     } else {
//                         alert('set primary image failed');
//                     }
//                 } catch (error) {
//                     alert('set primary image failed due to technical reasons');
//                 }
//             } else if (action === "delete") {
//                 try {
//                     const response = await fetch(`${window.location.href}/image/${imageId}`, {
//                         method: 'DELETE',
//                     });
//                     if (response.ok) {
//                         alert("delete image success");
//                         window.location.reload();
//                     } else if (response.status === 400) {
//                         alert('cannot delete primary image');
//                     } else {
//                         alert('delete image failed');
//                     }
//                 } catch (error) {
//                     alert('delete image failed due to technical reasons');
//                 }
//             }
//         })
//     })
// })

// document.getElementById('uploadBtn').addEventListener('click', function (e) {
//     const imageInput = document.getElementById('imageInput');
//     if (imageInput.files.length === 0) {
//         alert('Please select a file to upload');
//         return;
//     }
//
//     const formData = new FormData();
//     const imageFile = imageInput.files[0];
//     formData.append('image', imageFile);
//
//     fetch(`${window.location.href}/image`, {
//         method: 'POST',
//         body: formData,
//     })
//         .then(response => {
//             if (response.ok) {
//                 alert('Image uploaded successfully');
//                 window.location.reload();
//                 return response.json();
//             }
//             throw new Error('Network response was not ok.');
//         })
//         .catch(error => {
//             console.error('There has been a problem with your fetch operation:', error);
//         });
// });
//
document.getElementById('upload-guide-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    // 获取用户输入的邮箱和密码
    var type = document.querySelector('input[name="type"]:checked').value;
    var existsInNZ = document.querySelector('input[name="exists-in-nz"]:checked').value;
    var cn = document.getElementById('common-name').value;
    var sn = document.getElementById('scientific-name').value;
    var kc = document.getElementById('key-characteristics').value;
    var description = document.getElementById('description').value;
    var symptoms = document.getElementById('symptoms').value;

    console.log()

    var data = {
        type:type,
        exists_in_nz:existsInNZ,
        common_name:cn,
        scientific_name:sn,
        key_characteristics:kc,
        description:description,
        symptoms:symptoms
    };

    console.log(data)
    return;
    try {
        const response = await fetch(`/staff/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert("update staff profile success");
            window.location.reload();
        } else {
            alert("update staff profile failed");
            return;
        }
    } catch (error) {
        console.error('Error:', error);
        alert('update staff profile failed due to technical reasons.');
    }
});