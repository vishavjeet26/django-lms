from rest_framework import permissions
from django.db.models import Q

class IsAdminOrReadOnly(permissions.BasePermission):
    # Custom permission to only allow Admin of an object to edit it.
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the Admin.
        print("IsAdminOrReadOnly class calling")
        return is_admin_user(request)


class IsAdminStaffOrReadOnly(permissions.BasePermission):
    # Custom permission to only allow Admin or Staff of an object to edit it.
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the Admin, Staff and Student of the LMS.
        print("IsAdminStaffOrReadOnly")
        return is_admin_staff_user(request)
      
class IsAdminStaffStudentOrReadOnly(permissions.BasePermission):
    # Custom permission to only allow Admin, Staff  or Student of an object to edit it.
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the Admin, Staff and Student of the LMS.
        print("IsAdminStaffStudentOrReadOnly")
        return is_admin_staff_student_user(request)

"""
Custom permission function to only allow Admin of an object to create book,
assign book, delete book, update book, get all books, get all users
assign book, and submit ot user.
"""
def is_admin_user(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='admin').exists():
            print("Admin login...")
            return True
    return False   

"""
Custom permission to only allow Staff of an object to create book, see all books,
assign book and submit ot user.
"""
def is_admin_staff_user(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(Q(name='admin') | Q(name='staff')).exists():
            print("Staff login...")
            return True
    return False        

"""
Custom permission to only allow admin, staff and student of an object to see all books,
check book status, create assign request
"""
def is_admin_staff_student_user(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(Q(name='admin') | Q(name='staff') | Q(name='student')).exists():
            print("student login...")
            return True
    return False         