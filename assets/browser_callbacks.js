window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside_charts: {
        render_charts: function (data) {
            // Check if data is available
            if (!data) {
                return;
            }

            // Ensure the container exists before initializing the chart
            const chartContainer = document.getElementById('echarts-container');
            if (!chartContainer) {
                return;
            }

            // Initialize the chart using ECharts with locale set to English
            const myChart = echarts.init(chartContainer, null, { locale: 'EN' });

            // Set the chart options using the passed data
            myChart.setOption(data);

            // Ensure the chart resizes properly with the window size
            window.addEventListener("resize", () => {
                myChart.resize();
            });
        }
    }
});
