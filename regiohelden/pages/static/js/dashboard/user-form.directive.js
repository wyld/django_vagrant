angular.module('usersApp')
    .directive('userForm', userForm);

function userForm(usersService) {
    return {
        restrict: 'E',
        templateUrl: '/static/templates/user-edit-form.html',
        link: link,
        scope: {
            visible: '=',
            editedUserData: '=',
            editedUserId: '=',
            callback: '&'
        }
    };

    function link($scope) {
        $scope.formSubmit = function(editedUserId, editedUserData){
            editedUserData.submitted = true;
            if (!editedUserId) {
                usersService.addUser(editedUserData).then(function(data){
                    if (data.errors) {
                        editedUserData.errors = {};
                        angular.forEach(data.errors, function(value, key){
                            editedUserData.errors[key] = value;
                        })
                    } else {
                        console.log($scope.callback);
                        $scope.callback({user: data});
                        $scope.visible = false;
                    }
                })
            }
        }

        $scope.formTitle = function(){
            if (!$scope.editedUserId) {
                return 'Add user';
            }
            return 'Edit user';
        }
    }
}