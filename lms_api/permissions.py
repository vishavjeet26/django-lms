from rest_framework import permissions
from django.db.models import Q

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow Admin of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the Admin.
        return request.user.groups.filter(name='admin').exists()

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow Staff of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the Staff of the book.
        return request.user.groups.filter(name='staff').exists()
       # return 0

class IsStudentOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the Student of the book.
        return request.user.groups.filter(name='student').exists()

class IsAdminStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow Admin or Staff of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the Admin, Staff and Student of the LMS.
        return request.user.groups.filter(Q(name='admin') | Q(name='staff')).exists()
      
class IsAdminStaffStudentOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow Admin, Staff  or Student of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the Admin, Staff and Student of the LMS.
        return request.user.groups.filter(Q(name='admin') | Q(name='staff') | Q(name='student')).exists()