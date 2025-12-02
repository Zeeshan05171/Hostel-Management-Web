"""
Custom permissions for role-based access control.
"""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Permission class: Only Admin users can access"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsWarden(permissions.BasePermission):
    """Permission class: Only Warden users can access"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_warden


class IsStudent(permissions.BasePermission):
    """Permission class: Only Student users can access"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_student


class IsAdminOrWarden(permissions.BasePermission):
    """Permission class: Admin or Warden users can access"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_admin or request.user.is_warden
        )
