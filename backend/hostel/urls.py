"""
URL configuration for hostel app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet, basename='room')
router.register(r'students', views.StudentProfileViewSet, basename='student')
router.register(r'fees', views.FeeViewSet, basename='fee')
router.register(r'attendance', views.AttendanceViewSet, basename='attendance')
router.register(r'visitors', views.VisitorViewSet, basename='visitor')
router.register(r'complaints', views.ComplaintViewSet, basename='complaint')
router.register(r'mess-menu', views.MessMenuViewSet, basename='mess-menu')
router.register(r'contact', views.ContactMessageViewSet, basename='contact')

urlpatterns = [
    # Dashboard stats
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    
    # Router URLs
    path('', include(router.urls)),
]
