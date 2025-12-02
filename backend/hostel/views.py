"""
Views for hostel management API endpoints.
CRUD operations with role-based access control.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import date

from .models import Room, StudentProfile, Fee, Attendance, Visitor, Complaint, MessMenu, ContactMessage
from .serializers import (
    RoomSerializer, StudentProfileSerializer, StudentProfileCreateSerializer,
    FeeSerializer, AttendanceSerializer, VisitorSerializer,
    ComplaintSerializer, MessMenuSerializer, ContactMessageSerializer,
    DashboardStatsSerializer
)
from accounts.permissions import IsAdmin, IsAdminOrWarden


class RoomViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Rooms.
    Admin: Full access
    Warden: Read only
    Student: Read only
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['room_no', 'room_type']
    ordering_fields = ['room_no', 'floor', 'status']
    
    def get_permissions(self):
        """Only admins can create, update, or delete"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Filter by status if provided"""
        queryset = Room.objects.all()
        status_filter = self.request.query_params.get('status', None)
        room_type = self.request.query_params.get('type', None)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if room_type:
            queryset = queryset.filter(room_type=room_type)
        
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def update_status(self, request, pk=None):
        """Update room status"""
        room = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Room.STATUS_CHOICES).keys():
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        room.status = new_status
        room.save()
        
        return Response(RoomSerializer(room).data)


class StudentProfileViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Student Profiles.
    Admin: Full access
    Warden: Read only
    Student: Read own profile only
    """
    queryset = StudentProfile.objects.select_related('user', 'room').all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StudentProfileCreateSerializer
        return StudentProfileSerializer
    
    def get_permissions(self):
        """Only admins can create, update, or delete"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Filter based on user role"""
        user = self.request.user
        queryset = StudentProfile.objects.select_related('user', 'room').all()
        
        # Students can only see their own profile
        if user.is_student:
            queryset = queryset.filter(user=user)
        
        # Filter by active status if provided
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by fee status
        fee_status = self.request.query_params.get('fee_status', None)
        if fee_status:
            queryset = queryset.filter(fees__status=fee_status).distinct()
        
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def assign_room(self, request, pk=None):
        """Assign room to student"""
        student = self.get_object()
        room_id = request.data.get('room_id')
        
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if room is available
        if not room.is_available:
            return Response({'error': 'Room is not available'}, status=status.HTTP_400_BAD_REQUEST)
        
        student.room = room
        student.save()
        
        return Response(StudentProfileSerializer(student).data)


class FeeViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Fees.
    Admin: Full access
    Warden: Read only
    Student: Read own fees only
    """
    queryset = Fee.objects.select_related('student__user').all()
    serializer_class = FeeSerializer
    
    def get_permissions(self):
        """Only admins can create, update, or delete"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Filter based on user role"""
        user = self.request.user
        queryset = Fee.objects.select_related('student__user').all()
        
        # Students can only see their own fees
        if user.is_student and hasattr(user, 'student_profile'):
            queryset = queryset.filter(student=user.student_profile)
        
        # Filter by status
        fee_status = self.request.query_params.get('status', None)
        if fee_status:
            queryset = queryset.filter(status=fee_status)
        
        # Filter by student
        student_id = self.request.query_params.get('student_id', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def mark_paid(self, request, pk=None):
        """Mark fee as paid"""
        fee = self.get_object()
        payment_method = request.data.get('payment_method', '')
        
        fee.status = Fee.PAID
        fee.paid_date = timezone.now().date()
        fee.payment_method = payment_method
        fee.save()
        
        return Response(FeeSerializer(fee).data)


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Attendance.
    Admin/Warden: Can mark and view
    Student: Read own attendance only
    """
    queryset = Attendance.objects.select_related('student__user', 'marked_by').all()
    serializer_class = AttendanceSerializer
    
    def get_permissions(self):
        """Admins and wardens can create/update"""
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAdminOrWarden()]
        elif self.action == 'destroy':
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Filter based on user role"""
        user = self.request.user
        queryset = Attendance.objects.select_related('student__user', 'marked_by').all()
        
        # Students can only see their own attendance
        if user.is_student and hasattr(user, 'student_profile'):
            queryset = queryset.filter(student=user.student_profile)
        
        # Filter by date
        date_filter = self.request.query_params.get('date', None)
        if date_filter:
            queryset = queryset.filter(date=date_filter)
        
        # Filter by student
        student_id = self.request.query_params.get('student_id', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set marked_by to current user"""
        serializer.save(marked_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get attendance summary for a student"""
        student_id = request.query_params.get('student_id', None)
        
        if not student_id:
            if request.user.is_student and hasattr(request.user, 'student_profile'):
                student_id = request.user.student_profile.id
            else:
                return Response({'error': 'student_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        total = Attendance.objects.filter(student_id=student_id).count()
        present = Attendance.objects.filter(student_id=student_id, status=Attendance.PRESENT).count()
        absent = Attendance.objects.filter(student_id=student_id, status=Attendance.ABSENT).count()
        leave = Attendance.objects.filter(student_id=student_id, status=Attendance.LEAVE).count()
        
        percentage = (present / total * 100) if total > 0 else 0
        
        return Response({
            'total_days': total,
            'present': present,
            'absent': absent,
            'leave': leave,
            'percentage': round(percentage, 2)
        })


class VisitorViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Visitors.
    Admin/Warden: Full access
    Student: Read own visitors only
    """
    queryset = Visitor.objects.select_related('student__user', 'approved_by').all()
    serializer_class = VisitorSerializer
    
    def get_permissions(self):
        """Admins and wardens can create/update/delete"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrWarden()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Filter based on user role"""
        user = self.request.user
        queryset = Visitor.objects.select_related('student__user', 'approved_by').all()
        
        # Students can only see their own visitors
        if user.is_student and hasattr(user, 'student_profile'):
            queryset = queryset.filter(student=user.student_profile)
        
        # Filter by student
        student_id = self.request.query_params.get('student_id', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        # Filter by today's visitors
        today_only = self.request.query_params.get('today', None)
        if today_only:
            queryset = queryset.filter(in_time__date=date.today())
        
        return queryset
    
    def perform_create(self, serializer):
        """Set approved_by to current user"""
        serializer.save(approved_by=self.request.user)


class ComplaintViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Complaints.
    Admin/Warden: Full access
    Student: Can create and view own complaints
    """
    queryset = Complaint.objects.select_related('student__user', 'resolved_by').all()
    serializer_class = ComplaintSerializer
    
    def get_permissions(self):
        """Students can create, Admins/Wardens can update"""
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminOrWarden()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Filter based on user role"""
        user = self.request.user
        queryset = Complaint.objects.select_related('student__user', 'resolved_by').all()
        
        # Students can only see their own complaints
        if user.is_student and hasattr(user, 'student_profile'):
            queryset = queryset.filter(student=user.student_profile)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by student
        student_id = self.request.query_params.get('student_id', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set student to current user's profile"""
        if self.request.user.is_student:
            serializer.save(student=self.request.user.student_profile)
        else:
            serializer.save()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrWarden])
    def resolve(self, request, pk=None):
        """Mark complaint as resolved"""
        complaint = self.get_object()
        resolution_notes = request.data.get('resolution_notes', '')
        
        complaint.status = Complaint.RESOLVED
        complaint.resolved_by = request.user
        complaint.resolution_notes = resolution_notes
        complaint.save()
        
        return Response(ComplaintSerializer(complaint).data)


class MessMenuViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Mess Menu.
    Admin: Full access
    Others: Read only
    """
    queryset = MessMenu.objects.all()
    serializer_class = MessMenuSerializer
    
    def get_permissions(self):
        """Only admins can create, update, or delete"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Filter by date if provided"""
        queryset = MessMenu.objects.all()
        date_filter = self.request.query_params.get('date', None)
        
        if date_filter:
            queryset = queryset.filter(date=date_filter)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's menu"""
        try:
            menu = MessMenu.objects.get(date=date.today())
            return Response(MessMenuSerializer(menu).data)
        except MessMenu.DoesNotExist:
            return Response({'message': 'No menu for today'}, status=status.HTTP_404_NOT_FOUND)


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Contact Messages.
    Anyone: Can create
    Admin: Can view all
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    
    def get_permissions(self):
        """Anyone can create, only admins can view/update"""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdmin()]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    GET /api/dashboard/stats/
    Get dashboard statistics based on user role
    """
    user = request.user
    
    # Base stats
    stats = {
        'total_rooms': Room.objects.count(),
        'occupied_rooms': Room.objects.filter(status=Room.OCCUPIED).count(),
        'available_rooms': Room.objects.filter(status=Room.VACANT).count(),
        'total_students': StudentProfile.objects.count(),
        'active_students': StudentProfile.objects.filter(is_active=True).count(),
    }
    
    # Admin/Warden specific stats
    if user.is_admin or user.is_warden:
        stats.update({
            'pending_fees': Fee.objects.filter(Q(status=Fee.UNPAID) | Q(status=Fee.OVERDUE)).count(),
            'total_fees_amount': Fee.objects.aggregate(total=Sum('amount'))['total'] or 0,
            'paid_fees_amount': Fee.objects.filter(status=Fee.PAID).aggregate(total=Sum('amount'))['total'] or 0,
            'todays_visitors': Visitor.objects.filter(in_time__date=date.today()).count(),
            'pending_complaints': Complaint.objects.filter(status=Complaint.PENDING).count(),
            'todays_attendance': Attendance.objects.filter(date=date.today(), status=Attendance.PRESENT).count(),
        })
    
    # Student specific stats
    if user.is_student and hasattr(user, 'student_profile'):
        profile = user.student_profile
        stats = {
            'room': RoomSerializer(profile.room).data if profile.room else None,
            'pending_fees': Fee.objects.filter(student=profile, status__in=[Fee.UNPAID, Fee.OVERDUE]).count(),
            'total_attendance': Attendance.objects.filter(student=profile).count(),
            'present_days': Attendance.objects.filter(student=profile, status=Attendance.PRESENT).count(),
            'pending_complaints': Complaint.objects.filter(student=profile, status=Complaint.PENDING).count(),
        }
    
    serializer = DashboardStatsSerializer(stats)
    return Response(serializer.data)
