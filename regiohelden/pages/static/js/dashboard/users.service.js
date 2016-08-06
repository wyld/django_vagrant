angular.module('usersApp')
    .factory('usersService', usersService);

function usersService($http) {
    var baseApiUrl = '/api/1.0/users/';

    return {
        getUsersList: getUsersList,
    };

    function getUsersList() {
        return $http.get(baseApiUrl)
            .then(function(result) {
                return result.data.results;
            });
    }
}