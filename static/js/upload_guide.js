document.getElementById('upload-guide-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    var type = document.querySelector('input[name="type"]:checked').value;
    var existsInNZ = document.querySelector('input[name="exists-in-nz"]:checked').value;
    var cn = document.getElementById('common-name').value;
    var sn = document.getElementById('scientific-name').value;
    var kc = document.getElementById('key-characteristics').value;
    var description = document.getElementById('description').value;
    var symptoms = document.getElementById('symptoms').value;

    console.log()

    var data = {
        type: type,
        exists_in_nz: existsInNZ,
        common_name: cn,
        scientific_name: sn,
        key_characteristics: kc,
        description: description,
        symptoms: symptoms
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