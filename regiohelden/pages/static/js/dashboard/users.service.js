angular.module('usersApp')
    .factory('usersService', usersService);

function usersService($http) {
    var baseApiUrl = '/api/1.0/users/';

    return {
        getUsersList: getUsersList,
        addUser: addUser,
    };

    function getUsersList() {
        return $http.get(baseApiUrl)
            .then(function(result) {
                return result.data.results;
            });
    }

    function addUser(userData) {
        var data = {
            first_name: userData.first_name,
            last_name: userData.last_name,
            iban: userData.iban
        };

        return $http.post(baseApiUrl, data)
            .then(function(result) {
                return result.data;
            },
            function(result){
                var data = {};
                data.errors = result.data;

                return data;
            });
    }
}