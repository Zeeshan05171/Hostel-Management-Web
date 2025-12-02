"""
Database models for Hostel Management System.
Includes: Room, StudentProfile, Fee, Attendance, Visitor, Complaint, MessMenu, ContactMessage
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


class Room(models.Model):
    """Model for hostel rooms"""
    
    # Room type choices
    SINGLE = 'single'
    DOUBLE = 'double'
    TRIPLE = 'triple'
    
    ROOM_TYPE_CHOICES = [
        (SINGLE, 'Single'),
        (DOUBLE, 'Double'),
        (TRIPLE, 'Triple'),
    ]
    
    # Status choices
    VACANT = 'vacant'
    OCCUPIED = 'occupied'
    MAINTENANCE = 'maintenance'
    
    STATUS_CHOICES = [
        (VACANT, 'Vacant'),
        (OCCUPIED, 'Occupied'),
        (MAINTENANCE, 'Under Maintenance'),
    ]
    
    room_no = models.CharField(max_length=10, unique=True, help_text='Room number')
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, default=DOUBLE)
    capacity = models.IntegerField(default=2, help_text='Maximum number of students')
    floor = models.IntegerField(default=1, help_text='Floor number')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=VACANT)
    description = models.TextField(blank=True, null=True, help_text='Additional room details')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['room_no']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
    
    def __str__(self):
        return f"Room {self.room_no} ({self.get_room_type_display()})"
    
    @property
    def current_occupancy(self):
        """Get current number of students in room"""
        return self.students.filter(is_active=True).count()
    
    @property
    def is_available(self):
        """Check if room has available space"""
        return self.status == self.VACANT and self.current_occupancy < self.capacity


class StudentProfile(models.Model):
    """Extended profile for students"""
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        help_text='Assigned room'
    )
    contact = models.CharField(max_length=15, help_text='Student contact number')
    emergency_contact = models.CharField(max_length=15, help_text='Emergency contact number')
    father_name = models.CharField(max_length=100, help_text='Father\'s name')
    address = models.TextField(help_text='Permanent address')
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_joining = models.DateField(default=timezone.now, help_text='Date joined hostel')
    is_active = models.BooleanField(default=True, help_text='Active student status')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_of_joining']
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"
    
    def save(self, *args, **kwargs):
        """Update room status when student is assigned"""
        super().save(*args, **kwargs)
        if self.room and self.is_active:
            # Update room status to occupied if it has students
            if self.room.current_occupancy > 0 and self.room.status == Room.VACANT:
                self.room.status = Room.OCCUPIED
                self.room.save()


class Fee(models.Model):
    """Model for fee management"""
    
    # Payment status choices
    UNPAID = 'unpaid'
    PAID = 'paid'
    OVERDUE = 'overdue'
    
    STATUS_CHOICES = [
        (UNPAID, 'Unpaid'),
        (PAID, 'Paid'),
        (OVERDUE, 'Overdue'),
    ]
    
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='fees'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Fee amount')
    due_date = models.DateField(help_text='Payment due date')
    paid_date = models.DateField(null=True, blank=True, help_text='Date payment received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=UNPAID)
    payment_method = models.CharField(max_length=50, blank=True, null=True, help_text='Payment method')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-due_date']
        verbose_name = 'Fee'
        verbose_name_plural = 'Fees'
    
    def __str__(self):
        return f"{self.student.user.username} - ${self.amount} ({self.get_status_display()})"
    
    def save(self, *args, **kwargs):
        """Auto-update status to overdue if past due date"""
        if self.status == self.UNPAID and self.due_date < timezone.now().date():
            self.status = self.OVERDUE
        super().save(*args, **kwargs)


class Attendance(models.Model):
    """Model for daily attendance tracking"""
    
    # Attendance status choices
    PRESENT = 'present'
    ABSENT = 'absent'
    LEAVE = 'leave'
    
    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (LEAVE, 'On Leave'),
    ]
    
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    date = models.DateField(default=timezone.now, help_text='Attendance date')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PRESENT)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='marked_attendance'
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        unique_together = ['student', 'date']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.date} ({self.get_status_display()})"


class Visitor(models.Model):
    """Model for visitor management"""
    
    visitor_name = models.CharField(max_length=100, help_text='Visitor name')
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='visitors'
    )
    purpose = models.CharField(max_length=200, help_text='Purpose of visit')
    contact = models.CharField(max_length=15, help_text='Visitor contact number')
    in_time = models.DateTimeField(default=timezone.now, help_text='Check-in time')
    out_time = models.DateTimeField(null=True, blank=True, help_text='Check-out time')
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_visitors'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-in_time']
        verbose_name = 'Visitor'
        verbose_name_plural = 'Visitors'
    
    def __str__(self):
        return f"{self.visitor_name} visiting {self.student.user.username}"


class Complaint(models.Model):
    """Model for complaints and maintenance requests"""
    
    # Status choices
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    RESOLVED = 'resolved'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (RESOLVED, 'Resolved'),
    ]
    
    # Priority choices
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]
    
    # Category choices
    ELECTRICAL = 'electrical'
    PLUMBING = 'plumbing'
    CLEANING = 'cleaning'
    MAINTENANCE = 'maintenance'
    OTHER = 'other'
    
    CATEGORY_CHOICES = [
        (ELECTRICAL, 'Electrical'),
        (PLUMBING, 'Plumbing'),
        (CLEANING, 'Cleaning'),
        (MAINTENANCE, 'Maintenance'),
        (OTHER, 'Other'),
    ]
    
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='complaints'
    )
    title = models.CharField(max_length=200, help_text='Complaint title')
    description = models.TextField(help_text='Detailed description')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=OTHER)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=MEDIUM)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=PENDING)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_complaints'
    )
    resolution_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"


class MessMenu(models.Model):
    """Model for daily mess menu"""
    
    date = models.DateField(unique=True, help_text='Menu date')
    breakfast = models.TextField(help_text='Breakfast items')
    lunch = models.TextField(help_text='Lunch items')
    snacks = models.TextField(blank=True, null=True, help_text='Evening snacks')
    dinner = models.TextField(help_text='Dinner items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Mess Menu'
        verbose_name_plural = 'Mess Menus'
    
    def __str__(self):
        return f"Menu for {self.date}"


class ContactMessage(models.Model):
    """Model for contact form messages"""
    
    name = models.CharField(max_length=100, help_text='Sender name')
    email = models.EmailField(help_text='Sender email')
    role = models.CharField(max_length=20, help_text='Sender role')
    message = models.TextField(help_text='Message content')
    is_resolved = models.BooleanField(default=False, help_text='Message resolved status')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"Message from {self.name} ({self.email})"
