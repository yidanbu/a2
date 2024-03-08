document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll(".staff-delete");
    buttons.forEach(button => {
        button.addEventListener('click', async function (e) {
            e.preventDefault();

            const staffID = button.getAttribute("value");
            try {
                const response = await fetch(`${staffID}`, {
                    method: 'DELETE',
                });
                if (response.ok) {
                    alert("delete staff success");
                    window.location.reload();
                } else {
                    alert('delete staff failed');
                }
            } catch (error) {
                console.log(error)
                alert('delete staff failed due to technical reasons');
            }
        })
    })
})