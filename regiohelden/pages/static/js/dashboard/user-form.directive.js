angular.module('usersApp')
    .directive('userForm', userForm);

function userForm(usersService) {
    return {
        restrict: 'E',
        templateUrl: '/static/templates/user-edit-form.html',
        link: link,
        scope: {
            visible: '=',
            formUser: '=',
            callback: '&'
        }
    };

    function link($scope) {
        $scope.formSubmit = function(formUser){
            formUser.submitted = true;
            if (!formUser.id) {
                usersService.addUser(formUser).then(function(data){
                    if (data.errors) {
                        formUser.errors = {};
                        angular.forEach(data.errors, function(value, key){
                            formUser.errors[key] = value;
                        })
                    } else {
                        $scope.callback({user: data});
                        $scope.visible = false;
                    }
                })
            } else {
                usersService.updateUser(formUser).then(function(data){
                    if (data.errors) {
                        formUser.errors = {};
                        angular.forEach(data.errors, function(value, key){
                            formUser.errors[key] = value;
                        })
                    } else {
                        $scope.callback({user: data});
                        $scope.visible = false;
                    }
                })
            }
        }

        $scope.formCancel = function() {
            $scope.visible = false;
        }

        $scope.formTitle = function(){
            if ($scope.formUser && $scope.formUser.id) {
                return 'Edit user';
            }
            return 'Add user';
        }
    }
}