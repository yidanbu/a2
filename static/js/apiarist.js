// Create delete button and related function for apiarist
document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll(".apiarist-delete");
    buttons.forEach(button => {
        button.addEventListener('click', async function (e) {
            e.preventDefault();

            const apiaristID = button.getAttribute("value");
            try {
                const response = await fetch(`${apiaristID}`, {
                    method: 'DELETE',
                });
                if (response.ok) {
                    alert("delete apiarist success");
                    window.location.reload();
                } else {
                    alert('delete apiarist failed');
                }
            } catch (error) {
                console.log(error)
                alert('delete apiarist failed due to technical reasons');
            }
        })
    })
})