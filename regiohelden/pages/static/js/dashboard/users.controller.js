angular.module('usersApp')
    .controller('usersController', usersController);

function usersController($scope, usersService, Constants) {
    initialize();

    function initialize() {
        $scope.users = [];
        $scope.formVisible = false;
        $scope.currentUser = Constants.currentUser;

        usersService.getUsersList().then(function(users){
            $scope.users = users;
        });
    }

    $scope.showAddUser = function() {
    	if (!$scope.formVisible) {
    		$scope.formVisible = true;
    		$scope.editedUserData = {first_name: '', last_name: '', iban: ''};
    		$scope.editedUserId = null;
    	}
    }

    $scope.deleteUser = function(user) {
    	usersService.deleteUser(user).then(function(data){
    		if (data.success) {
    			var index = $scope.users.indexOf(user);
    			if (index > -1) {
				    $scope.users.splice(index, 1);
				}
    		}
    	})
    }

    $scope.addUserCallback = function(user) {
    	$scope.users.push(user);
    }
}