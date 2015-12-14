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

routerApp.run(function (server, $location, $rootScope) {
    $location.path('/system-status');
});

