/**
 * Created by root on 12/11/15.
 */

var routerApp = angular.module('routerApp', ['ngRoute']);

routerApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.when('/loading', {
            templateUrl: '/static/app/loading.html',
        }).when('/load-status', {
            templateUrl: '/static/app/load-status.html'
        }).when('/cpu-status', {
            templateUrl: '/static/app/cpu-status.html'
        }).when('/memory-status', {
            templateUrl: '/static/app/memory-status.html'
        }).otherwise({
            redirectTo: '/loading'
        });
    }
]);

routerApp.directive('navBar', function ($location) {
    return {
        restrict: 'E',
        templateUrl: '/static/app/navbar.html',
        link: function (scope) {
            scope.items = [
                'load-status',
                'cpu-status',
                'memory-status'
            ];

            scope.getNavItemName = function (url) {
                return url.replace('-', ' ');
            };

            scope.isActive = function (route) {
                return '/' + route === $location.path();
            };
        }
    }
});

routerApp.directive('loader', function () {
    return {
        restrict: 'E',
        scope: {
            width: "@"
        },
        template: '<div class="spinner">' + '<div class="bounce1"></div>' + '<div class="bounce2"></div>' + '<div class="bounce3"></div>' + '</div>'
    };
});

routerApp.directive('topBar', function () {
    return {
        restrict: 'E',
        scope: {
            heading: '=',
            refresh: '&',
            lastUpdated: '=',
            info: '=',
        },
        templateUrl: '/static/app/top-bar.html',
        link: function (scope, element, attrs) {
            var $refreshBtn = element.find('refresh-btn').eq(0);

            if (typeof attrs.noRefreshBtn !== 'undefined') {
                $refreshBtn.remove();
            }
        }
    };
});

routerApp.directive('refreshBtn', function () {
    return {
        restrict: 'E',
        scope: {
            refresh: '&'
        },
        template: '<button ng-click="refresh()">&olarr;</button>'
    };
});

routerApp.directive('noData', function () {
    return {
        restrict: 'E',
        template: 'No Data'
    };
});

routerApp.directive('lastUpdate', function () {
    return {
        restrict: 'E',
        scope: {
            timestamp: '='
        },
        templateUrl: '/static/app/last-update.html'
    };
});

routerApp.directive('keyValueList', ['server', '$rootScope', function (server, $rootScope) {
    return {
        restrict: 'E',
        scope: {
            heading: '@',
            info: '@',
            moduleName: '@',
        },
        templateUrl: '/static/app/key-value-list.html',
        link: function (scope, element) {
            scope.getData = function () {
                delete scope.tableRows;

                server.get(scope.moduleName, function (serverResopnseData) {
                    scope.tableRows = serverResopnseData;
                    scope.lastGet = new Date().getTime();

                    if (Object.keys(serverResopnseData).length == 0) {
                        scope.emptyResult = true;
                    }

                    if (!scope.$$phase && !$rootScope.$$phase) {
                        scope.$digest();
                    }
                });
            };

            scope.getData();
        }
    };
}]);

routerApp.directive('plugin', function () {
    return {
        restrict: 'E',
        transclude: true,
        templateUrl: '/static/app/base-plugin.html'
    };
});

routerApp.directive('multiLineChart', ['$interval', '$compile', 'server', function ($interval, $compile, server) {
    return {
        restrict: 'E',
        scope: {
            heading: '@',
            moduleName: '@',
            refreshRate: '=',
            getDisplayValue: '=',
            delay: '='
        },
        templateUrl: '/static/app/multi-line-chart.html',
        link: function (scope, element) {
            var chart = new SmoothieChart({
                borderVisible: false,
                sharpLines: true,
                grid: {
                    fillStyle: '#ffffff',
                    strokeStyle: 'rgba(232, 230, 230, 0.93)',
                    sharpLines: true,
                    borderVisible: false
                },
                labels: {
                    fontSize: 12,
                    precision: 0,
                    fillStyle: '#0f0e0e'
                },
                maxValue: 100,
                minValue: 0,
                horizontalLines: [{
                    value: 1,
                    color: '#ecc',
                    lineWidth: 1
                }]
            });

            var seriesOptions = [{
                strokeStyle: 'rgba(255, 0, 0, 1)',
                lineWidth: 2
            }, {
                strokeStyle: 'rgba(0, 255, 0, 1)',
                lineWidth: 2
            }, {
                strokeStyle: 'rgba(0, 0, 255, 1)',
                lineWidth: 2
            }, {
                strokeStyle: 'rgba(255, 255, 0, 1)',
                lineWidth: 1
            }, {
                strokeStyle: 'rgba(255, 0, 255, 1)',
                lineWidth: 1
            }, {
                strokeStyle: 'rgba(0, 0, 0, 1)',
                lineWidth: 1
            }, {
                strokeStyle: 'rgba(0, 255, 255, 1)',
                lineWidth: 1
            }, {
                strokeStyle: 'rgba(255, 0, 125, 1)',
                lineWidth: 1
            }, {
                strokeStyle: 'rgba(255, 125, 0, 1)',
                lineWidth: 1
            }, {
                strokeStyle: 'rgba(125, 255, 0, 1)',
                lineWidth: 1
            }];

            var canvas = element.find('canvas')[0];
            scope.seriesArray = [];
            scope.metricsArray = [];

            server.get(scope.moduleName, function (serverResponseData) {
                var numberOfLines = Object.keys(serverResponseData).length;

                for (var x = 0; x < numberOfLines; x++) {
                    var keyForThisLine = Object.keys(serverResponseData)[x];

                    scope.seriesArray[x] = new TimeSeries();
                    chart.addTimeSeries(scope.seriesArray[x], seriesOptions[x]);
                    scope.metricsArray[x] = {
                        name: keyForThisLine,
                        color: seriesOptions[x].strokeStyle,
                    };
                }
            });

            var delay = 1000;

            if (angular.isDefined(scope.delay)) {
                delay = scope.delay;
            }

            chart.streamTo(canvas, delay);

            var dataCallInProgress = false;

            scope.getData = function () {
                if (dataCallInProgress) return;

                if (!scope.seriesArray.length) return;

                dataCallInProgress = true;

                server.get(scope.moduleName, function (serverResponseData) {
                    dataCallInProgress = false;
                    scope.lastGet = new Date().getTime();
                    var keyCount = 0;
                    var maxAvg = 1;

                    for (var key in serverResponseData) {
                        scope.seriesArray[keyCount].append(scope.lastGet, serverResponseData[key]);
                        keyCount++;
                        maxAvg = Math.max(maxAvg, serverResponseData[key]);
                    }

                    scope.metricsArray.forEach(function (metricObj) {
                        metricObj.data = serverResponseData[metricObj.name].toString();
                    });

                    var len = parseInt(Math.log(maxAvg) / Math.log(10));
                    var div = Math.pow(10, len);
                    chart.options.maxValue = Math.ceil(maxAvg / div) * div;
                });
            };

            var refreshRate = (angular.isDefined(scope.refreshRate)) ? scope.refreshRate : 1000;
            var intervalRef = $interval(scope.getData, refreshRate);
            var removeInterval = function () {
                $interval.cancel(intervalRef);
            };

            element.on('$destroy', removeInterval);
        }
    }
}]);

routerApp.directive('cpuAvgLoadChart', ['server', function (server) {
    return {
        restrict: 'E',
        scope: {},
        templateUrl: '/static/app/cpu-load.html'
    };
}]);

routerApp.directive('cpuChart', ['server', function (server) {
    return {
        restrict: 'E',
        scope: {},
        templateUrl: '/static/app/cpu-chart.html'
    };
}]);

routerApp.directive('memoryChart', ['server', function (server) {
    return {
        restrict: 'E',
        scope: {},
        templateUrl: '/static/app/memory-chart.html'
    };
}]);

var simpleTableModules = [
    {
        name: 'memoryInfo',
        template: '<key-value-list heading="内存信息(B)" module-name="memory" info="/proc/meminfo 文件读出"></key-value-list>'
    }, {
        name: 'cpuInfo',
        template: '<key-value-list heading="CPU信息(%)" module-name="cpu" info="/proc/stats 文件读出"></key-value-list>'
    }, {
        name: 'loadInfo',
        template: '<key-value-list heading="负载信息" module-name="load" info="/proc/avgload 文件读出"></key-value-list>'
    }, {
        name: 'loadSplineChart',
        template: '<spline-chart-load heading="负载趋势图" collection-name="one_min_load" unit=""></spline-chart-load>'
    }, {
        name: 'cpuSplineChart',
        template: '<spline-chart-cpu heading="CPU趋势图" collection-name="one_min_cpu" unit="%"></spline-chart-cpu>'
    }, {
        name: 'memorySplineChart',
        template: '<spline-chart-memory heading="内存趋势图" collection-name="one_min_memory" unit="B"></spline-chart-memory>'
    }
];

simpleTableModules.forEach(function (module, key) {

    routerApp.directive(module.name, ['server', function (server) {

        var moduleDirective = {
            restrict: 'E',
            scope: {}
        };

        if (module.template) {
            moduleDirective['template'] = module.template;
        }

        return moduleDirective;
    }]);

});

Highcharts.setOptions({
    global: {
        useUTC: false
    }
});

var ids = ['load', 'cpu', 'memory'];

ids.forEach(function (mod, key) {
    var name = mod.replace(/^\S/, function (s) {
        return s.toUpperCase()
    });

    routerApp.directive('splineChart' + name, ['$interval', '$compile', 'performance', function ($interval, $compile, performance) {
        return {
            restrict: 'E',
            scope: {
                heading: '@',
                collectionName: '@',
                unit: '@',
                refreshRate: '='
            },
            templateUrl: '/static/app/spline-chart-' + mod + '.html',
            link: function (scope, element, attrs) {
                scope.isOne = true;
                scope.isFive = false;
                scope.isThirty = false;
                scope.isDay = false;

                scope.reset = function () {
                    var slength = scope.highcharts.series.length;
                    for (var i = 0; i < slength; i++) {
                        scope.highcharts.series[0].remove();
                    }
                }

                scope.onemin = function () {
                    scope.isOne = true;
                    scope.isFive = false;
                    scope.isThirty = false;
                    scope.isDay = false;

                    removeInterval();
                    refreshRate = 60 * 1000;
                    scope.collectionName = 'one_min_' + mod;
                    scope.getData();
                    intervalRef = $interval(scope.getData, refreshRate);
                }

                scope.fivemin = function () {
                    scope.isOne = false;
                    scope.isFive = true;
                    scope.isThirty = false;
                    scope.isDay = false;

                    removeInterval();
                    refreshRate = 5 * 60 * 1000;
                    scope.collectionName = 'five_min_' + mod;
                    scope.getData();
                    intervalRef = $interval(scope.getData, refreshRate);
                }

                scope.thirtymin = function () {
                    scope.isOne = false;
                    scope.isFive = false;
                    scope.isThirty = true;
                    scope.isDay = false;

                    removeInterval();
                    refreshRate = 30 * 60 * 1000;
                    scope.collectionName = 'thirty_min_' + mod;
                    scope.getData();
                    intervalRef = $interval(scope.getData, refreshRate);
                }

                scope.oneday = function () {
                    scope.isOne = false;
                    scope.isFive = false;
                    scope.isThirty = false;
                    scope.isDay = true;

                    removeInterval();
                    refreshRate = 24 * 60 * 60 * 1000;
                    scope.collectionName = 'one_day_' + mod;
                    scope.getData();
                    intervalRef = $interval(scope.getData, refreshRate);
                }

                scope.highcharts = new Highcharts.Chart({
                    chart: {
                        renderTo: mod,
                        type: 'spline',
                        height: 480,
                        width: 800
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
                                return this.value + scope.unit;
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
                            return '<b>' + this.series.name + '</b><br>'
                                + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x)
                                + '<br>' + Highcharts.numberFormat(this.y, 2) + scope.unit;
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

                scope.getData = function () {
                    scope.lastGet = new Date().getTime();

                    performance.get(scope.collectionName, function (serverResponseData) {
                        var obj = serverResponseData;
                        if (obj.length != 0) {
                            ddata = [];
                            for (var i = 0; i < length(obj[0].data); i++) {
                                ddata[i] = new Array();
                            }

                            keys = [];
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

                            slength = scope.highcharts.series.length;

                            if (slength == 0) {
                                for (var i = 0; i < ddata.length; i++) {
                                    scope.highcharts.addSeries({
                                        name: keys[i],
                                        data: ddata[i]
                                    });
                                }
                            } else {
                                for (var i = 0; i < slength; i++) {
                                    scope.highcharts.series[i].setData(ddata[i]);
                                }
                            }
                        } else {
                            if (scope.highcharts.series.length != 0) {
                                scope.reset();
                                removeInterval();
                            }
                        }
                    });
                };

                function length(o) {
                    var count = 0;
                    for (var i in o) {
                        count++;
                    }
                    return count;
                }

                scope.getData();
                var refreshRate = (angular.isDefined(scope.refreshRate)) ? scope.refreshRate : 60 * 1000;
                var intervalRef = $interval(scope.getData, refreshRate);
                var removeInterval = function () {
                    $interval.cancel(intervalRef);
                };

                element.on('$destroy', removeInterval);
            }
        }
    }]);

});