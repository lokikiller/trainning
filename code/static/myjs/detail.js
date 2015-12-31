/**
 * Created by root on 15-12-30.
 */

$(function () {
    var loadChart;
    drawLoadLine('one_min_load');

    var cpuChart;
    drawCpuLine('one_min_cpu');

    var memoryChart;
    drawMemoryLine('one_min_memory');

    loadTimer = setInterval(function () {
        drawLoadLine('one_min_load');
    }, 60 * 1000);

    cpuTimer = setInterval(function () {
        drawCpuLine('one_min_cpu');
    }, 60 * 1000);

    memoryTimer = setInterval(function () {
        drawMemoryLine('one_min_memory');
    }, 60 * 1000);
})

$('#onemin').on('click', function (event) {
    event.preventDefault();
    $('.btn-monitor').removeClass('selected');
    $(this).addClass('selected');
    onemin();
});

function onemin() {
    window.clearInterval(loadTimer);
    window.clearInterval(cpuTimer);
    window.clearInterval(memoryTimer);

    drawLoadLine('one_min_load');
    drawCpuLine('one_min_cpu');
    drawMemoryLine('one_min_memory');

    loadTimer = setInterval(function () {
        drawLoadLine('one_min_load');
    }, 60 * 1000);

    cpuTimer = setInterval(function () {
        drawCpuLine('one_min_cpu');
    }, 60 * 1000);

    memoryTimer = setInterval(function () {
        drawMemoryLine('one_min_memory');
    }, 60 * 1000);
}

$('#fivemin').on('click', function (event) {
    event.preventDefault();
    $('.btn-monitor').removeClass('selected');
    $(this).addClass('selected');
    fivemin();
});

function fivemin() {
    window.clearInterval(loadTimer);
    window.clearInterval(cpuTimer);
    window.clearInterval(memoryTimer);

    drawLoadLine('five_min_load');
    drawCpuLine('five_min_cpu');
    drawMemoryLine('five_min_memory');

    loadTimer = setInterval(function () {
        drawLoadLine('five_min_load');
    }, 5 * 60 * 1000);

    cpuTimer = setInterval(function () {
        drawCpuLine('five_min_cpu');
    }, 5 * 60 * 1000);

    memoryTimer = setInterval(function () {
        drawMemoryLine('five_min_memory');
    }, 5 * 60 * 1000);
}

$('#thirtymin').on('click', function (event) {
    event.preventDefault();
    $('.btn-monitor').removeClass('selected');
    $(this).addClass('selected');
    thirtymin();
});

function thirtymin() {
    window.clearInterval(loadTimer);
    window.clearInterval(cpuTimer);
    window.clearInterval(memoryTimer);

    drawLoadLine('thirty_min_load');
    drawCpuLine('thirty_min_cpu');
    drawMemoryLine('thirty_min_memory');

    loadTimer = setInterval(function () {
        drawLoadLine('thirty_min_load');
    }, 30 * 60 * 1000);

    cpuTimer = setInterval(function () {
        drawCpuLine('thirty_min_cpu');
    }, 30 * 60 * 1000);

    memoryTimer = setInterval(function () {
        drawMemoryLine('thirty_min_memory');
    }, 30 * 60 * 1000);
}

$('#oneday').on('click', function (event) {
    event.preventDefault();
    $('.btn-monitor').removeClass('selected');
    $(this).addClass('selected');
    oneday();
});

function oneday() {
    window.clearInterval(loadTimer);
    window.clearInterval(cpuTimer);
    window.clearInterval(memoryTimer);

    drawLoadLine('one_day_load');
    drawCpuLine('one_day_cpu');
    drawMemoryLine('one_day_memory');

    loadTimer = setInterval(function () {
        drawLoadLine('one_day_load');
    }, 24 * 60 * 60 * 1000);

    cpuTimer = setInterval(function () {
        drawCpuLine('one_day_cpu');
    }, 24 * 60 * 60 * 1000);

    memoryTimer = setInterval(function () {
        drawMemoryLine('one_day_memory');
    }, 24 * 60 * 60 * 1000);
}

function drawLoadLine(types) {
    var uuid = $('#maindiv').attr("uuid");
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });

    loadChart = new Highcharts.Chart({
        chart: {
            renderTo: 'loadpic',
            type: 'spline',
            animation: Highcharts.svg,
            height: 400,
            events: {
                load: function () {

                }
            }
        },
        title: {
            text: ''
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: ''
            },
            labels: {
                formatter: function () {
                    return this.value;
                }
            }
        },
        plotOptions: {
            spline: {
                lineWidth: 2.0,
                fillOpacity: 0.1,
                marker: {
                    enabled: false,
                    states: {
                        hover: {
                            enabled: true,
                            radius: 2
                        }
                    }
                },
                shadow: false
            }
        },
        tooltip: {
            formatter: function () {
                return '<b>Load' + this.series.name + '</b><br>'
                    + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x)
                    + '<br>' + Highcharts.numberFormat(this.y, 2);
            }

        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: []
    });

    updateLoadData(uuid, types);
}

function updateLoadData(uuid, type) {
    $.ajax({
        type: 'get',
        url: '/performance',
        data: {
            uuid: uuid,
            collection: type
        },
        dataType: 'text',
        success: function (response) {
            var obj = jQuery.parseJSON(response);
            if (obj.length != 0) {
                var ddata = [];
                for (var i = 0; i < length(obj[0].data); i++) {
                    ddata[i] = new Array();
                }

                var keys = [];
                for (key in obj[0].data) {
                    keys.push(key);
                }

                for (key in obj) {
                    var dtime = obj[key].time;
                    i = 0;
                    for (k in obj[key].data) {
                        ddata[i].push({
                            x: dtime * 1000,
                            y: parseFloat(obj[key].data[k])
                        });
                        i++;
                    }
                }

                var slength = loadChart.series.length;

                if (slength == 0) {
                    for (var i = 0; i < ddata.length; i++) {
                        loadChart.addSeries({
                            name: keys[i],
                            data: ddata[i]
                        });
                    }
                } else {
                    for (var i = 0; i < slength; i++) {
                        loadChart.series[i].setData(ddata[i]);
                    }
                }
            } else {
                if (loadChart.series.length != 0) {
                    var slength = loadChart.series.length;
                    for (var i = 0; i < slength; i++) {
                        loadChart.series[0].remove();
                    }
                }
            }
        }
    });
}

function drawCpuLine(types) {
    var uuid = $('#maindiv').attr("uuid");
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });

    cpuChart = new Highcharts.Chart({
        chart: {
            renderTo: 'cpupic',
            type: 'spline',
            animation: Highcharts.svg,
            height: 400,
            events: {
                load: function () {

                }
            }
        },
        title: {
            text: ''
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: ''
            },
            min: 0,
            labels: {
                formatter: function () {
                    return this.value + '%';
                }
            }
        },
        plotOptions: {
            spline: {
                lineWidth: 2.0,
                fillOpacity: 0.1,
                marker: {
                    enabled: false,
                    states: {
                        hover: {
                            enabled: true,
                            radius: 2
                        }
                    }
                },
                shadow: false
            }
        },
        tooltip: {
            formatter: function () {
                return '<b>CPU' + this.series.name + '</b><br>'
                    + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x)
                    + '<br>' + Highcharts.numberFormat(this.y, 5) + '%';
            }

        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: []
    });

    updateCpuData(uuid, types);
}

function updateCpuData(uuid, type) {
    $.ajax({
        type: 'get',
        url: '/performance',
        data: {
            uuid: uuid,
            collection: type
        },
        dataType: 'text',
        success: function (response) {
            var obj = jQuery.parseJSON(response);
            if (obj.length != 0) {
                var ddata = [];
                for (var i = 0; i < length(obj[0].data); i++) {
                    ddata[i] = new Array();
                }

                var keys = [];
                for (key in obj[0].data) {
                    keys.push(key);
                }

                for (key in obj) {
                    var dtime = obj[key].time;
                    i = 0;
                    for (k in obj[key].data) {
                        ddata[i].push({
                            x: dtime * 1000,
                            y: parseFloat(obj[key].data[k])
                        });
                        i++;
                    }
                }

                var slength = cpuChart.series.length;

                if (slength == 0) {
                    for (var i = 0; i < ddata.length; i++) {
                        cpuChart.addSeries({
                            name: keys[i],
                            data: ddata[i]
                        });
                    }
                } else {
                    for (var i = 0; i < slength; i++) {
                        cpuChart.series[i].setData(ddata[i]);
                    }
                }
            } else {
                if (cpuChart.series.length != 0) {
                    var slength = cpuChart.series.length;
                    for (var i = 0; i < slength; i++) {
                        cpuChart.series[0].remove();
                    }
                }
            }
        }
    });
}

function drawMemoryLine(types) {
    var uuid = $('#maindiv').attr("uuid");
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });

    memoryChart = new Highcharts.Chart({
        chart: {
            renderTo: 'memorypic',
            type: 'spline',
            animation: Highcharts.svg,
            height: 400,
            events: {
                load: function () {

                }
            }
        },
        title: {
            text: ''
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: ''
            },
            min: 0,
            labels: {
                formatter: function () {
                    return this.value + 'GB';
                }
            }
        },
        plotOptions: {
            spline: {
                lineWidth: 2.0,
                fillOpacity: 0.1,
                marker: {
                    enabled: false,
                    states: {
                        hover: {
                            enabled: true,
                            radius: 2
                        }
                    }
                },
                shadow: false
            }
        },
        tooltip: {
            formatter: function () {
                return '<b>Memory' + this.series.name + '</b><br>'
                    + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x)
                    + '<br>' + Highcharts.numberFormat(this.y, 5) + 'GB';
            }
        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: []
    });

    updateMemoryData(uuid, types);
}

function updateMemoryData(uuid, type) {
    $.ajax({
        type: 'get',
        url: '/performance',
        data: {
            uuid: uuid,
            collection: type
        },
        dataType: 'text',
        success: function (response) {
            var obj = jQuery.parseJSON(response);
            if (obj.length != 0) {
                var ddata = [];
                for (var i = 0; i < length(obj[0].data); i++) {
                    ddata[i] = new Array();
                }

                var keys = [];
                for (key in obj[0].data) {
                    keys.push(key);
                }

                for (key in obj) {
                    var dtime = obj[key].time;
                    i = 0;
                    for (k in obj[key].data) {
                        ddata[i].push({
                            x: dtime * 1000,
                            y: parseFloat(obj[key].data[k] / (1024 * 1024 * 1024))
                        });
                        i++;
                    }
                }

                var slength = memoryChart.series.length;

                if (slength == 0) {
                    for (var i = 0; i < ddata.length; i++) {
                        memoryChart.addSeries({
                            name: keys[i],
                            data: ddata[i]
                        });
                    }
                } else {
                    for (var i = 0; i < slength; i++) {
                        memoryChart.series[i].setData(ddata[i]);
                    }
                }
            } else {
                if (memoryChart.series.length != 0) {
                    var slength = memoryChart.series.length;
                    for (var i = 0; i < slength; i++) {
                        memoryChart.series[0].remove();
                    }
                }
            }
        }
    });
}

function length(o) {
    var count = 0;
    for (var i in o) {
        count++;
    }
    return count;
}