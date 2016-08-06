angular.module('usersApp')
    .factory('usersService', usersService);

function usersService($http) {
    var baseApiUrl = '/api/1.0/users/';

    return {
        getUsersList: getUsersList,
        addUser: addUser,
        updateUser: updateUser,
        deleteUser: deleteUser
    };

    function getUserUrl(user) {
        return baseApiUrl + user.id + '/';
    }

    function getUsersList() {
        return $http.get(baseApiUrl)
            .then(function(result) {
                return result.data.results;
            });
    }

    function addUser(user) {
        var data = {
            first_name: user.first_name,
            last_name: user.last_name,
            iban: user.iban
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

    function updateUser(user) {
        var userUrl = getUserUrl(user);
        var data = {
            first_name: user.first_name,
            last_name: user.last_name,
            iban: user.iban
        };

        return $http.patch(userUrl, data)
            .then(function(result) {
                return result.data;
            },
            function(result){
                var data = {};
                data.errors = result.data;

                return data;
            });
    }

    function deleteUser(user) {
        var userUrl = getUserUrl(user);

        return $http.delete(userUrl)
            .then(function(result) {
                return {success: true}
            },
            function(result){
                return {success: false}
            });
    }
}