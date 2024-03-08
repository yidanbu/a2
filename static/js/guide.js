document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll(".guide-delete");
    buttons.forEach(button => {
        button.addEventListener('click', async function (e) {
            e.preventDefault();

            const guideID = button.getAttribute("value");
            try {
                const response = await fetch(`${guideID}`, {
                    method: 'DELETE',
                });
                if (response.ok) {
                    alert("delete guide success");
                    window.location.reload();
                } else {
                    alert('delete guide failed');
                }
            } catch (error) {
                console.log(error)
                alert('delete guide failed due to technical reasons');
            }
        })
    })
})