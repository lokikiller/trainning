/**
 * Created by root on 12/11/15.
 */

routerApp.service('server', ['$http', '$rootScope', '$location', function ($http, $rootScope, $location) {

    this.get = function (moduleName, callback) {
        var moduleAddress = 'server/?module=' + moduleName;

        return $http.get(moduleAddress).then(function (response) {
            return callback(response.data);
        });
    };

}]);

routerApp.service('performance', ['$http', '$rootScope', '$location', function ($http, $rootScope, $location) {
    this.get = function (collectionName, callback) {
        var collectionAddress = 'performance/?collection=' + collectionName;

        return $http.get(collectionAddress).then(function (response) {
            return callback(response.data);
        });
    }
}]);


routerApp.run(function (server, $location, $rootScope) {
    var currentRoute = $location.path();
    var currentTab = (currentRoute == '/loading') ? 'load-status': currentRoute;
    localStorage.setItem('currentTab', currentTab);

    $location.path('/load-status');
});
