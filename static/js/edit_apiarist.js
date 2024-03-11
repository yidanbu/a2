document.getElementById('edit-apiarist-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    var id = document.getElementById('id').value
    var firstName = document.getElementById('first-name').value;
    var lastName = document.getElementById('last-name').value;
    var address = document.getElementById('address').value;
    var email = document.getElementById('email').value;
    var phone = document.getElementById('phone').value
    var status = document.querySelector('input[name="status"]:checked').value
    var data = {
        first_name: firstName,
        last_name: lastName,
        address: address,
        email: email,
        phone: phone,
        status: status
    };

    console.log(data)
    try {
        const response = await fetch(`/apiarist/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert("update apiarist profile success");
            window.location.reload();
        } else {
            alert("update apiarist profile failed");
            return;
        }
    } catch (error) {
        console.error('Error:', error);
        alert('update apiarist profile failed due to technical reasons.');
    }
});