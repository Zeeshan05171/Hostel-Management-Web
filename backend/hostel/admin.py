"""
Admin configuration for hostel app.
"""
from django.contrib import admin
from .models import Room, StudentProfile, Fee, Attendance, Visitor, Complaint, MessMenu, ContactMessage


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_no', 'room_type', 'capacity', 'floor', 'status', 'current_occupancy']
    list_filter = ['room_type', 'status', 'floor']
    search_fields = ['room_no']
    ordering = ['room_no']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'contact', 'date_of_joining', 'is_active']
    list_filter = ['is_active', 'date_of_joining']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'contact']
    ordering = ['-date_of_joining']


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount', 'due_date', 'status', 'paid_date']
    list_filter = ['status', 'due_date']
    search_fields = ['student__user__username']
    ordering = ['-due_date']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'marked_by']
    list_filter = ['status', 'date']
    search_fields = ['student__user__username']
    ordering = ['-date']


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['visitor_name', 'student', 'purpose', 'in_time', 'out_time']
    list_filter = ['in_time']
    search_fields = ['visitor_name', 'student__user__username']
    ordering = ['-in_time']


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'category', 'priority', 'status', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['title', 'student__user__username']
    ordering = ['-created_at']


@admin.register(MessMenu)
class MessMenuAdmin(admin.ModelAdmin):
    list_display = ['date', 'breakfast', 'lunch', 'dinner']
    ordering = ['-date']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'role', 'is_resolved', 'created_at']
    list_filter = ['is_resolved', 'role', 'created_at']
    search_fields = ['name', 'email', 'message']
    ordering = ['-created_at']
