angular.module('usersApp')
    .controller('usersController', usersController);

function usersController($scope, usersService) {
    initialize();

    function initialize() {
        $scope.users = [];
        $scope.formVisible = false;

        usersService.getUsersList().then(function(users){
            $scope.users = users;
        });
    }

    $scope.showAddUser = function(){
    	if (!$scope.formVisible) {
    		$scope.formVisible = true;
    		$scope.editedUserData = {first_name: '', last_name: '', iban: ''};
    		$scope.editedUserId = null;
    	}
    }

    $scope.addUserCallback = function(user){
    	$scope.users.push(user);
    }
}