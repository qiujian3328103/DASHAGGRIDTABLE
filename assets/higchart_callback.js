window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside_highchart: {
        render_charts: function (data, plot_type) {
            // Check if data is available
            if (!data) {
                return;
            }

            // Parse the JSON string into an array of objects
            const parsedData = JSON.parse(data);

            // Group data by the unique 'group_col' values
            const groupedData = {};
            parsedData.forEach(item => {
                if (!groupedData[item.group_col]) {
                    groupedData[item.group_col] = [];
                }
                // Store [x, y] values for the scatter plot using `date` as the x value
                groupedData[item.group_col].push([item.date, item.value]);
            });

            // Ensure the container exists before initializing the chart
            const chartContainer = document.getElementById('highchart-container');
            if (!chartContainer) {
                return;
            }

            // Define a color palette (or Highcharts will use its default palette)
            const colors = Highcharts.getOptions().colors;

            // Create a series configuration for each unique 'group_col' group
            const seriesData = Object.keys(groupedData).map((group, index) => ({
                name: group,                 // Series name is the group_col value
                color: colors[index % colors.length],  // Assign a color from the palette
                data: groupedData[group],    // Data points for this group
                marker: {
                    radius: 5
                }
            }));

            // Extract unique dates for x-axis categories
            const uniqueDates = [...new Set(parsedData.map(item => item.date))];

            // Highcharts configuration for scatter plot
            Highcharts.chart(chartContainer, {
                chart: {
                    type: 'scatter',
                    zoomType: 'xy'
                },
                title: {
                    text: 'Scatter Plot: Value vs Date Colored by Group Column'
                },
                xAxis: {
                    title: {
                        text: 'Date'
                    },
                    categories: uniqueDates,  // Use the `date` values as x-axis labels
                    tickInterval: 1,
                    labels: {
                        rotation: -45,  // Rotate x-axis labels for better readability
                    }
                },
                yAxis: {
                    title: {
                        text: 'Value'
                    }
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',     // Align legend to the right side
                    verticalAlign: 'middle',  // Position legend in the middle right
                    floating: true,
                    backgroundColor: Highcharts.defaultOptions.chart.backgroundColor,
                    borderWidth: 1
                },
                plotOptions: {
                    scatter: {
                        marker: {
                            radius: 5,
                            states: {
                                hover: {
                                    enabled: true,
                                    lineColor: 'rgb(100,100,100)'
                                }
                            }
                        },
                        states: {
                            hover: {
                                marker: {
                                    enabled: false
                                }
                            }
                        },
                        tooltip: {
                            headerFormat: '<b>{series.name}</b><br>',
                            pointFormat: 'Date: {point.x}, Value: {point.y}'
                        }
                    }
                },
                series: seriesData // Use the formatted series data for the scatter plot
            });

            // Ensure the chart resizes properly with the window size
            window.addEventListener("resize", () => {
                Highcharts.charts.forEach(chart => chart.reflow());
            });
        }
    }
});
