"""
User model with role-based access control for Hostel Management System.
Roles: Admin, Warden, Student
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds role field for access control.
    """
    
    # Role choices
    ADMIN = 'admin'
    WARDEN = 'warden'
    STUDENT = 'student'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (WARDEN, 'Warden'),
        (STUDENT, 'Student'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT,
        help_text='User role for access control'
    )
    
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text='Contact phone number'
    )
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        """Check if user is an admin"""
        return self.role == self.ADMIN
    
    @property
    def is_warden(self):
        """Check if user is a warden"""
        return self.role == self.WARDEN
    
    @property
    def is_student(self):
        """Check if user is a student"""
        return self.role == self.STUDENT
