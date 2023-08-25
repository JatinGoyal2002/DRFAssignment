from rest_framework import permissions


# Create your views here.
class StaffUserPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.auth == None:
            return False
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
            if request.user.is_staff == False:
                return False
        return True