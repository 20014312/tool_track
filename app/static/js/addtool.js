document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("addtoolForm").addEventListener("submit", function (event) {
        event.preventDefault();

        const title = document.getElementById("title").value;
        console.log("Title", title);

        const formData = new FormData();
        formData.append("title", document.getElementById("title").value);
        formData.append("description", document.getElementById("description").value);
        formData.append("toolImage", document.getElementById("toolImage").files[0]);


        fetch('/addtool', {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const message = document.getElementById("message");
            if (data.success) {
                message.textContent = "Tool added successfully!";
                message.style.color = "green";
                document.getElementById("addtoolForm").reset();
            } else {
                message.textContent = "Error adding tool.";
                message.style.color = "red";
            }
        })
        .catch(error => console.error("Error:", error));
    });
});