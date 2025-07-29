document.addEventListener("DOMContentLoaded", function () {
    fetch('/get_my_tools')
        .then(response => response.json())
        .then(data => {
            const toolsContainer = document.getElementById("toolsContainer");
            toolsContainer.innerHTML = "";

            if (!data) {
                toolsContainer.innerHTML = "<p>You haven't added any tools yet.</p>";
                return;
            }

            if (data.tools.length === 0) {
                toolsContainer.innerHTML = "<p>You haven't added any tools yet.</p>";
                return;
            }

            console.log("Data:::" + data.tools.length)

            data.tools.forEach(tool => {
                const toolCard = document.createElement("div");
                toolCard.classList.add("tool-card");

                toolCard.innerHTML = `
                    <img src="${imageUrl + tool.image}" alt="${tool.username}" class="card-image">
                    <h3>${tool.name}</h3>
                    <p><strong>Status:</strong> ${tool.status}</p>
                    <button class="delete-tool">Delete</button>
                `;

                toolsContainer.appendChild(toolCard);


                const deleteBtn = toolCard.querySelector('.delete-tool');
                deleteBtn.addEventListener('click', (event) => {
                    event.stopPropagation();
                    const confirmDelete = confirm(`Are you sure you want to delete "${tool.title}"?`);
                    if (confirmDelete) {
                        fetch(`/delete_tool/${tool.tool_id}`)
                            .then(response => {
                                if (response.ok) {
                                    toolCard.remove();
                                    location.reload();
                                } else {
                                    console.error('Failed to delete tool');
                                }
                            })
                            .catch(error => console.error('Error deleting tool:', error));
                    }
                });

            });
        })
        .catch(error => console.error("Error fetching tools:", error));

    document.getElementById("addtoolBtn").addEventListener("click", function () {
        window.location.href = "/addtool";
    });
});
