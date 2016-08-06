angular.module('usersApp')
    .controller('usersController', usersController);

function usersController($scope, $filter, usersService, Constants) {
    initialize();

    function initialize() {
        $scope.users = [];
        $scope.formVisible = false;
        $scope.currentUser = Constants.currentUser;
        $scope.formUser = {
        	first_name: '',
        	last_name: '',
        	iban: '',
        	id: null
        }

        usersService.getUsersList().then(function(users){
            $scope.users = users;
        });
    }

    $scope.addUser = function() {
    	if (!$scope.formVisible) {
    		$scope.formUser.first_name = '';
    		$scope.formUser.last_name = '';
    		$scope.formUser.iban = '';
    		$scope.formUser.id = null;
    		$scope.formUser.errors = {};
    		$scope.formUser.submitted = false;
    		$scope.formVisible = true;
    	}
    }

    $scope.editUser = function(user) {
    	if (!$scope.formVisible) {
    		$scope.formUser.first_name = user.first_name;
    		$scope.formUser.last_name = user.last_name;
    		$scope.formUser.iban = user.iban;
    		$scope.formUser.id = user.id;
    		$scope.formUser.errors = {};
    		$scope.formUser.submitted = false;
    		$scope.formVisible = true;
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

    $scope.addorUpdateUserCallback = function(user) {
		var existingUsers = $filter("filter")($scope.users, {id: user.id});
		if (existingUsers.length) {
			angular.forEach(existingUsers, function(existingUser){
                var index = $scope.users.indexOf(existingUser);
                $scope.users[index] = user;
            })
		} else {
			$scope.users.push(user);
		}
    }
}