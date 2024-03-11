// add event listener to the edit guide form.
// including set primary button and delete button for images
document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll(".image-action");
    buttons.forEach(button => {
        button.addEventListener('click', async function (e) {
            e.preventDefault();

            const buttonInfo = button.getAttribute("name");
            const fields = buttonInfo.split("-");
            if (fields[0] !== "image") {
                return;
            }
            const imageId = fields[1];
            const action = fields[2];
            if (action === "setprimary") {
                try {
                    const response = await fetch(`${window.location.href}/image/${imageId}/primary`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    });
                    if (response.ok) {
                        alert("set primary image success");
                        window.location.reload();
                    } else {
                        alert('set primary image failed');
                    }
                } catch (error) {
                    alert('set primary image failed due to technical reasons');
                }
            } else if (action === "delete") {
                try {
                    const response = await fetch(`${window.location.href}/image/${imageId}`, {
                        method: 'DELETE',
                    });
                    if (response.ok) {
                        alert("delete image success");
                        window.location.reload();
                    } else if (response.status === 400) {
                        alert('cannot delete primary image');
                    } else {
                        alert('delete image failed');
                    }
                } catch (error) {
                    alert('delete image failed due to technical reasons');
                }
            }
        })
    })
})

document.getElementById('uploadBtn').addEventListener('click', function (e) {
    const imageInput = document.getElementById('imageInput');
    if (imageInput.files.length === 0) {
        alert('Please select a file to upload');
        return;
    }

    const formData = new FormData();
    const imageFile = imageInput.files[0];
    formData.append('image', imageFile);

    fetch(`${window.location.href}/image`, {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            if (response.ok) {
                alert('Image uploaded successfully');
                window.location.reload();
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
});

document.getElementById('edit-guide-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    var id = document.getElementById('id').value;
    var type = document.querySelector('input[name="type"]:checked').value;
    var exists_in_nz = document.querySelector('input[name="exists-in-nz"]:checked').value;
    var cn = document.getElementById('common-name').value;
    var sn = document.getElementById('scientific-name').value;
    var kc = document.getElementById('key-characteristics').value;
    var description = document.getElementById('description').value;
    var symptoms = document.getElementById('symptoms').value;
    var data = {
        type: type,
        exists_in_nz: exists_in_nz,
        common_name: cn,
        scientific_name: sn,
        key_characteristics: kc,
        description: description,
        symptoms: symptoms
    };
    console.log(data)
    try {
        const response = await fetch(`/guide/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert("update guide basic info success");
            window.location.reload();
        } else {
            alert("update guide basic info failed");
            return;
        }
    } catch (error) {
        console.error('Error:', error);
        alert('update guide basic info failed due to technical reasons.');
    }
});

// enable popover on disabled element
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))