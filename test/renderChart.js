// 在独立js脚本中定义比较长的回调函数
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        renderChart: (nClicks, data, id) => {

            // 源码参考：https://echarts.apache.org/examples/zh/editor.html?c=candlestick-brush

            // 根据id初始化绑定图表
            var myChart = echarts.init(document.getElementById(id));

            const upColor = '#00da3c';
            const downColor = '#ec0000';
            function splitData(rawData) {
                let categoryData = [];
                let values = [];
                let volumes = [];
                for (let i = 0; i < rawData.length; i++) {
                    categoryData.push(rawData[i].splice(0, 1)[0]);
                    values.push(rawData[i]);
                    volumes.push([i, rawData[i][4], rawData[i][0] > rawData[i][1] ? 1 : -1]);
                }
                return {
                    categoryData: categoryData,
                    values: values,
                    volumes: volumes
                };
            }
            function calculateMA(dayCount, data) {
                var result = [];
                for (var i = 0, len = data.values.length; i < len; i++) {
                    if (i < dayCount) {
                        result.push('-');
                        continue;
                    }
                    var sum = 0;
                    for (var j = 0; j < dayCount; j++) {
                        sum += data.values[i - j][1];
                    }
                    result.push(+(sum / dayCount).toFixed(3));
                }
                return result;
            }

            data = splitData(data);

            myChart.setOption(
                (option = {
                    animation: false,
                    legend: {
                        bottom: 10,
                        left: 'center',
                        data: ['Dow-Jones index', 'MA5', 'MA10', 'MA20', 'MA30']
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'cross'
                        },
                        borderWidth: 1,
                        borderColor: '#ccc',
                        padding: 10,
                        textStyle: {
                            color: '#000'
                        },
                        position: function (pos, params, el, elRect, size) {
                            const obj = {
                                top: 10
                            };
                            obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
                            return obj;
                        }
                    },
                    axisPointer: {
                        link: [
                            {
                                xAxisIndex: 'all'
                            }
                        ],
                        label: {
                            backgroundColor: '#777'
                        }
                    },
                    toolbox: {
                        feature: {
                            dataZoom: {
                                yAxisIndex: false
                            },
                            brush: {
                                type: ['lineX', 'clear']
                            }
                        }
                    },
                    brush: {
                        xAxisIndex: 'all',
                        brushLink: 'all',
                        outOfBrush: {
                            colorAlpha: 0.1
                        }
                    },
                    visualMap: {
                        show: false,
                        seriesIndex: 5,
                        dimension: 2,
                        pieces: [
                            {
                                value: 1,
                                color: downColor
                            },
                            {
                                value: -1,
                                color: upColor
                            }
                        ]
                    },
                    grid: [
                        {
                            left: '10%',
                            right: '8%',
                            height: '50%'
                        },
                        {
                            left: '10%',
                            right: '8%',
                            top: '63%',
                            height: '16%'
                        }
                    ],
                    xAxis: [
                        {
                            type: 'category',
                            data: data.categoryData,
                            boundaryGap: false,
                            axisLine: { onZero: false },
                            splitLine: { show: false },
                            min: 'dataMin',
                            max: 'dataMax',
                            axisPointer: {
                                z: 100
                            }
                        },
                        {
                            type: 'category',
                            gridIndex: 1,
                            data: data.categoryData,
                            boundaryGap: false,
                            axisLine: { onZero: false },
                            axisTick: { show: false },
                            splitLine: { show: false },
                            axisLabel: { show: false },
                            min: 'dataMin',
                            max: 'dataMax'
                        }
                    ],
                    yAxis: [
                        {
                            scale: true,
                            splitArea: {
                                show: true
                            }
                        },
                        {
                            scale: true,
                            gridIndex: 1,
                            splitNumber: 2,
                            axisLabel: { show: false },
                            axisLine: { show: false },
                            axisTick: { show: false },
                            splitLine: { show: false }
                        }
                    ],
                    dataZoom: [
                        {
                            type: 'inside',
                            xAxisIndex: [0, 1],
                            start: 98,
                            end: 100
                        },
                        {
                            show: true,
                            xAxisIndex: [0, 1],
                            type: 'slider',
                            top: '85%',
                            start: 98,
                            end: 100
                        }
                    ],
                    series: [
                        {
                            name: 'Dow-Jones index',
                            type: 'candlestick',
                            data: data.values,
                            itemStyle: {
                                color: upColor,
                                color0: downColor,
                                borderColor: undefined,
                                borderColor0: undefined
                            }
                        },
                        {
                            name: 'MA5',
                            type: 'line',
                            data: calculateMA(5, data),
                            smooth: true,
                            lineStyle: {
                                opacity: 0.5
                            }
                        },
                        {
                            name: 'MA10',
                            type: 'line',
                            data: calculateMA(10, data),
                            smooth: true,
                            lineStyle: {
                                opacity: 0.5
                            }
                        },
                        {
                            name: 'MA20',
                            type: 'line',
                            data: calculateMA(20, data),
                            smooth: true,
                            lineStyle: {
                                opacity: 0.5
                            }
                        },
                        {
                            name: 'MA30',
                            type: 'line',
                            data: calculateMA(30, data),
                            smooth: true,
                            lineStyle: {
                                opacity: 0.5
                            }
                        },
                        {
                            name: 'Volume',
                            type: 'bar',
                            xAxisIndex: 1,
                            yAxisIndex: 1,
                            data: data.volumes
                        }
                    ]
                }),
                true
            );
            myChart.dispatchAction({
                type: 'brush',
                areas: [
                    {
                        brushType: 'lineX',
                        coordRange: ['2016-06-02', '2016-06-20'],
                        xAxisIndex: 0
                    }
                ]
            });

            // 绑定刷选事件
            myChart.on(
                'brushEnd',
                (e) => {
                    // 更新数据到dash
                    window.dash_clientside.set_props(
                        'show-brush-range',
                        {
                            children: `刷选范围：${data.categoryData[e.areas[0].coordRange[0]]}, ${data.categoryData[e.areas[0].coordRange[1]]}`
                        }
                    )
                }
            )
            // 绑定缩略轴事件
            myChart.on(
                'datazoom',
                (e) => {
                    // 计算出当前缩放区间所对应的数据范围
                    var startIndex = Math.floor(e.start * data.categoryData.length / 100);
                    var endIndex = Math.ceil(e.end * data.categoryData.length / 100);
                    // 确保不会超出数组界限
                    startIndex = Math.max(startIndex, 0);
                    endIndex = Math.min(endIndex, data.categoryData.length - 1);
                    // 更新数据到dash
                    window.dash_clientside.set_props(
                        'show-slider-range',
                        {
                            children: `缩略轴范围：${data.categoryData[startIndex]}, ${data.categoryData[endIndex]}`
                        }
                    )
                }
            )

            window.addEventListener("resize", () => {
                myChart.resize();
            });
        }
    }
});