window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside_d3: {
        render_wafer_map: function (jsonData, ids) {
            if (!jsonData || !ids) {
                console.error("No data or ids provided.");
                return;
            }

            // Parse the JSON string back into an object
            console.log("Raw jsonData:", jsonData);  // Add logging
            const data = JSON.parse(jsonData);

            console.log("Parsed data:", data);  // Add logging
            console.log("IDs:", ids);  // Add logging

            ids.forEach(function(id) {
                const containerId = id['index'];
                const waferInfo = data[containerId];  // Get the correct wafer data and dimensions based on the ID
                console.log("Container ID:", containerId);  // Add logging
                if (!waferInfo || !waferInfo.wafer_data || !Array.isArray(waferInfo.wafer_data)) {
                    console.error("Invalid wafer data found for:", containerId);
                    return;
                }

                const waferData = waferInfo.wafer_data;
                const rectWidth = waferInfo.width;    // Use the width returned from the Python function
                const rectHeight = waferInfo.height;  // Use the height returned from the Python function

                // Call the drawWaferMap function to render the wafer map
                drawWaferMap(waferData, rectWidth, rectHeight, `wafer-container-${containerId}`);
            });
        }
    }
});


// Function to draw the wafer map using D3.js
function drawWaferMap(data, rectWidth, rectHeight, containerId) {
    if (!data || !Array.isArray(data)) {
        console.error("Invalid data for drawing wafer map.");
        return;
    }

    const svgContainer = document.getElementById(containerId);
    if (!svgContainer) {
        console.error("Container not found:", containerId);
        return;
    }

    // Clear the container if there is any existing SVG
    while (svgContainer.firstChild) {
        svgContainer.removeChild(svgContainer.firstChild);
    }

    const radius = 150;

    // Create the SVG element
    const svg = d3.create("svg")
        .attr("viewBox", [-radius, -radius, 2 * radius, 2 * radius])
        .style("width", "100%")
        .style("height", "100%");

    // Draw wafer circles
    svg.append("circle")
        .style("fill", "gray")
        .style("stroke", "black")
        .style("stroke-width", 0.025)
        .attr("r", radius)
        .attr("cx", 0.5)
        .attr("cy", 0.5);

    svg.append("circle")
        .style("fill", "lightgray")
        .style("stroke", "black")
        .style("stroke-width", 0.025)
        .attr("r", radius)
        .attr("cx", 0.5)
        .attr("cy", 0.5);

    // Check that data is defined and is an array
    svg.append("g").selectAll("rect")
        .data(data)
        .join("rect")
        .attr("x", d => d.x)
        .attr("y", d => d.y)
        .attr("width", rectWidth)  // Use dynamic width
        .attr("height", rectHeight)  // Use dynamic height
        .attr("fill", d => d.color)
        .attr("stroke", "white")
        .attr("stroke-width", 0.025)
        .append("title")
        .text(d => d.mouseover);

    // Add zoom functionality
    const zoom = d3.zoom()
        .scaleExtent([1, 8])
        .on("zoom", (event) => {
            svg.selectAll("circle, rect")
                .attr("transform", `scale(${event.transform.k})`);
        });

    svg.call(zoom);

    // Append the SVG to the container
    svgContainer.appendChild(svg.node());
}
