'''
Override rest framework permissions
'''
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
    

class IsStaffUserAuthenticated(permissions.BasePermission):
    """
    Here I'm checking if the request.user, if the request is coming from a group that is
    allowed to perform this action or if the user here is an staff member, aka admin user.
    You can check whatever you want here since you have access to the user. So you  can
    check the sales_department like you mentioned in the question.
    """
    def has_object_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return False