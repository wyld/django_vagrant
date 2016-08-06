from rest_framework import permissions


class OnlyCreatorCanModify(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user == obj.creator
