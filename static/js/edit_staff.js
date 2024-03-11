
document.getElementById('edit-staff-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    var id = document.getElementById('id').value
    var firstName = document.getElementById('first-name').value;
    var lastName = document.getElementById('last-name').value;
    var email = document.getElementById('email').value;
    var phone = document.getElementById('phone').value
    var position = document.getElementById('position').value
    var department = document.getElementById('department').value
    var status = document.querySelector('input[name="status"]:checked').value
    var role = document.querySelector('input[name="role"]:checked').value
    var data = {
        first_name: firstName,
        last_name: lastName,
        email: email,
        phone: phone,
        position: position,
        department: department,
        status: status,
        role: role
    };

    console.log(data)
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