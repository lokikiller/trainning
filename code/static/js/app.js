/**
 * Created by root on 12/11/15.
 */

var routerApp = angular.module('routerApp', ['ngRoute', 'highcharts-ng']);

routerApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.when('/loading', {
            templateUrl: '/static/app/loading.html',
        }).when('/system-status', {
            templateUrl: '/static/app/system-status.html'
        }).otherwise({
            redirectTo: '/loading'
        });
    }
]);

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

var simpleTableModules = [
    {
        name: 'memoryInfo',
        template: '<key-value-list heading="内存信息(B)" module-name="memory" info="/proc/meminfo 文件读出"></key-value-list>'
    }, {
        name: 'cpuInfo',
        template: '<key-value-list heading="CPU信息(%)" module-name="cpu" info="/proc/stats 文件读出"></key-value-list>'
    }, {
        name: 'loadSplineChart',
        template: '<spline-chart heading="load trend" collection-name="one_min_load"></spline-chart>'
    }, {
        name: 'cpuSplineChart',
        template: '<spline-chart heading="cpu trend" collection-name="one_min_cpu" unit="%"></spline-chart>'
    }, {
        name: 'memorySplineChart',
        template: '<spline-chart heading="memory trend" collection-name="one_min_memory" unit="B"></spline-chart>'
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


routerApp.directive('splineChart', ['$interval', '$compile', 'performance', function ($interval, $compile, performance) {
    return {
        restrict: 'E',
        scope: {
            heading: '@',
            collectionName: '@',
            inter: '@',
            intime: '@',
            unit: '@',
            refreshRate: '=',
        },
        templateUrl: '/static/app/spline-chart.html',
        link: function (scope, element) {
            scope.reset = function () {
                scope.highchartsNG.series = [];
            };

            scope.options = {
                type: 'spline'
            }

            scope.highchartsNG = {
                options: {
                    chart: {
                        type: 'spline'
                    },
                    global: {
                        useUTC: false
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
                        return '<b>' + scope.heading + this.series.name + '</b><br>'
                            + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x)
                            + '<br>' + Highcharts.numberFormat(this.y, 2) + scope.unit;
                    }
                },
                exporting: {
                    enabled: false
                },
                series: [],
                loading: false
            }

            scope.getData = function () {
                scope.reset()

                performance.get(scope.collectionName, function (serverResponseData) {
                    scope.lastGet = new Date().getTime();

                    var obj = serverResponseData;
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
                                x: dtime,
                                y: parseFloat(obj[key].data[k])
                            });
                            i++;
                        }
                    }

                    for (var i = 0; i < ddata.length; i++) {
                        scope.highchartsNG.series.push({
                            name: keys[i],
                            data: ddata[i]
                        });
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

            scope.getData();
        }
    }
}]);