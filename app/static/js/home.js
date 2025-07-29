document.addEventListener("DOMContentLoaded", async function () {
    const toolsList = document.getElementById("toolsList");

    async function fetchTools() {
        try {
            let response = await fetch(TOOLS_API_URL);
            let tools = await response.json();

            toolsList.innerHTML = "";
            tools.forEach(tool => {
                let toolCard = document.createElement("div");
                toolCard.classList.add("tool-card");

                console.log("ToolId:::"+tool.tool_id)

                toolCard.innerHTML = `
                    <img src="${imageUrl + tool.image}" alt="${tool.username}" class="card-image">
                    <h3>${tool.name}</h3>
                    <p>${tool.description}</p>
                    <button onclick="viewTool(${tool.tool_id})">View Details</button>
                `;

                toolsList.appendChild(toolCard);
            });

        } catch (error) {
            console.error("Error fetching tools:", error);
        }
    }

    fetchTools();
});

function viewTool(toolId) {
    window.location.href = `/view_tool/${toolId}`;
}