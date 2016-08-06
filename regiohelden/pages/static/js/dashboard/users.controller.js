angular.module('usersApp')
    .controller('usersController', usersController);

function usersController($scope, usersService) {
    initialize();

    function initialize() {
        $scope.users = [];

        usersService.getUsersList().then(function(users){
            $scope.users = users;
        });
    }
}