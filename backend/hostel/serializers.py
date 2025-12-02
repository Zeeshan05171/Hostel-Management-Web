"""
Serializers for hostel models.
"""
from rest_framework import serializers
from .models import Room, StudentProfile, Fee, Attendance, Visitor, Complaint, MessMenu, ContactMessage
from accounts.serializers import UserSerializer


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model"""
    
    current_occupancy = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Room
        fields = '__all__'


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serializer for StudentProfile model"""
    
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    room_details = RoomSerializer(source='room', read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = '__all__'


class StudentProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating student profile"""
    
    class Meta:
        model = StudentProfile
        fields = '__all__'


class FeeSerializer(serializers.ModelSerializer):
    """Serializer for Fee model"""
    
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_username = serializers.CharField(source='student.user.username', read_only=True)
    
    class Meta:
        model = Fee
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance model"""
    
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_username = serializers.CharField(source='student.user.username', read_only=True)
    marked_by_name = serializers.CharField(source='marked_by.get_full_name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'


class VisitorSerializer(serializers.ModelSerializer):
    """Serializer for Visitor model"""
    
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    
    class Meta:
        model = Visitor
        fields = '__all__'


class ComplaintSerializer(serializers.ModelSerializer):
    """Serializer for Complaint model"""
    
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    resolved_by_name = serializers.CharField(source='resolved_by.get_full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Complaint
        fields = '__all__'


class MessMenuSerializer(serializers.ModelSerializer):
    """Serializer for MessMenu model"""
    
    class Meta:
        model = MessMenu
        fields = '__all__'


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model"""
    
    class Meta:
        model = ContactMessage
        fields = '__all__'


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    
    total_rooms = serializers.IntegerField()
    occupied_rooms = serializers.IntegerField()
    available_rooms = serializers.IntegerField()
    total_students = serializers.IntegerField()
    active_students = serializers.IntegerField()
    pending_fees = serializers.IntegerField()
    total_fees_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    paid_fees_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    todays_visitors = serializers.IntegerField()
    pending_complaints = serializers.IntegerField()
    todays_attendance = serializers.IntegerField()
