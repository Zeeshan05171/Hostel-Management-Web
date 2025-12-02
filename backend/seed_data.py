"""
Seed data script for Hostel Management System.
Creates sample users, rooms, students, fees, attendance, visitors, complaints, and mess menus.

Run with: python manage.py shell < seed_data.py
Or: python manage.py shell
     >>> exec(open('seed_data.py').read())
"""
import os
import django
from datetime import datetime, timedelta, date
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from hostel.models import Room, StudentProfile, Fee, Attendance, Visitor, Complaint, MessMenu, ContactMessage

User = get_user_model()

def create_seed_data():
    print("🌱 Starting seed data creation...")
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    print("  Clearing existing data...")
    ContactMessage.objects.all().delete()
    MessMenu.objects.all().delete()
    Complaint.objects.all().delete()
    Visitor.objects.all().delete()
    Attendance.objects.all().delete()
    Fee.objects.all().delete()
    StudentProfile.objects.all().delete()
    Room.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    
    # ==================== USERS ====================
    print("  Creating users...")
    
    # Admin user
    admin = User.objects.create_user(
        username='admin',
        email='admin@hostelease.com',
        password='admin123',
        first_name='Admin',
        last_name='User',
        role=User.ADMIN,
        phone='03001234567'
    )
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    print(f"    ✓ Admin: {admin.username}")
    
    # Warden user
    warden = User.objects.create_user(
        username='warden',
        email='warden@hostelease.com',
        password='warden123',
        first_name='John',
        last_name='Smith',
        role=User.WARDEN,
        phone='03009876543'
    )
    print(f"    ✓ Warden: {warden.username}")
    
    # Student users
    students_data = [
        {'username': 'ali_khan', 'first_name': 'Ali', 'last_name': 'Khan', 'email': 'ali@student.com'},
        {'username': 'sara_ahmed', 'first_name': 'Sara', 'last_name': 'Ahmed', 'email': 'sara@student.com'},
        {'username': 'usman_malik', 'first_name': 'Usman', 'last_name': 'Malik', 'email': 'usman@student.com'},
        {'username': 'ayesha_raza', 'first_name': 'Ayesha', 'last_name': 'Raza', 'email': 'ayesha@student.com'},
        {'username': 'hassan_ali', 'first_name': 'Hassan', 'last_name': 'Ali', 'email': 'hassan@student.com'},
        {'username': 'fatima_shah', 'first_name': 'Fatima', 'last_name': 'Shah', 'email': 'fatima@student.com'},
        {'username': 'bilal_tariq', 'first_name': 'Bilal', 'last_name': 'Tariq', 'email': 'bilal@student.com'},
        {'username': 'zainab_iqbal', 'first_name': 'Zainab', 'last_name': 'Iqbal', 'email': 'zainab@student.com'},
    ]
    
    student_users = []
    for data in students_data:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password='student123',
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=User.STUDENT,
            phone=f'0300{1000000 + len(student_users)}'
        )
        student_users.append(user)
        print(f"    ✓ Student: {user.username}")
    
    # ==================== ROOMS ====================
    print("  Creating rooms...")
    
    rooms = []
    room_configs = [
        # Floor 1
        ('101', Room.SINGLE, 1, 1), ('102', Room.DOUBLE, 2, 1),
        ('103', Room.DOUBLE, 2, 1), ('104', Room.TRIPLE, 3, 1),
        ('105', Room.TRIPLE, 3, 1),
        # Floor 2
        ('201', Room.SINGLE, 1, 2), ('202', Room.DOUBLE, 2, 2),
        ('203', Room.DOUBLE, 2, 2), ('204', Room.TRIPLE, 3, 2),
        ('205', Room.TRIPLE, 3, 2),
        # Floor 3
        ('301', Room.SINGLE, 1, 3), ('302', Room.DOUBLE, 2, 3),
        ('303', Room.DOUBLE, 2, 3), ('304', Room.TRIPLE, 3, 3),
        ('305', Room.TRIPLE, 3, 3),
        # Floor 4
        ('401', Room.DOUBLE, 2, 4), ('402', Room.DOUBLE, 2, 4),
        ('403', Room.TRIPLE, 3, 4), ('404', Room.TRIPLE, 3, 4),
        ('405', Room.SINGLE, 1, 4),
    ]
    
    for room_no, room_type, capacity, floor in room_configs:
        room = Room.objects.create(
            room_no=room_no,
            room_type=room_type,
            capacity=capacity,
            floor=floor,
            status=Room.VACANT,
            description=f'{room_type.capitalize()} room on floor {floor}'
        )
        rooms.append(room)
    
    print(f"    ✓ Created {len(rooms)} rooms")
    
    # ==================== STUDENT PROFILES ====================
    print("  Creating student profiles...")
    
    student_profiles = []
    for i, user in enumerate(student_users):
        # Assign rooms to some students
        room = rooms[i % len(rooms)] if i < 10 else None
        
        profile = StudentProfile.objects.create(
            user=user,
            room=room,
            contact=user.phone,
            emergency_contact=f'0321{2000000 + i}',
            father_name=f'{user.last_name} Father',
            address=f'{i+1} Main Street, Lahore, Pakistan',
            date_of_birth=date(2000 + i, 1, 15),
            date_of_joining=date(2024, 9, 1),
            is_active=True
        )
        student_profiles.append(profile)
        print(f"    ✓ Profile: {user.username} -> Room {room.room_no if room else 'Unassigned'}")
    
    # ==================== FEES ====================
    print("  Creating fee records...")
    
    for i, profile in enumerate(student_profiles):
        # Monthly fee for current month
        Fee.objects.create(
            student=profile,
            amount=Decimal('15000.00'),
            due_date=date(2025, 12, 10),
            status=Fee.PAID if i % 3 == 0 else Fee.UNPAID,
            paid_date=date(2025, 12, 5) if i % 3 == 0 else None,
            payment_method='Bank Transfer' if i % 3 == 0 else None,
            notes='Monthly hostel fee'
        )
        
        # Previous month fee
        Fee.objects.create(
            student=profile,
            amount=Decimal('15000.00'),
            due_date=date(2025, 11, 10),
            status=Fee.PAID,
            paid_date=date(2025, 11, 8),
            payment_method='Cash',
            notes='Monthly hostel fee'
        )
    
    print(f"    ✓ Created {Fee.objects.count()} fee records")
    
    # ==================== ATTENDANCE ====================
    print("  Creating attendance records...")
    
    # Create attendance for last 30 days
    for i in range(30):
        attendance_date = date.today() - timedelta(days=i)
        for profile in student_profiles[:5]:  # Only for first 5 students
            import random
            status = random.choices(
                [Attendance.PRESENT, Attendance.ABSENT, Attendance.LEAVE],
                weights=[0.8, 0.15, 0.05]
            )[0]
            
            Attendance.objects.create(
                student=profile,
                date=attendance_date,
                status=status,
                marked_by=warden
            )
    
    print(f"    ✓ Created {Attendance.objects.count()} attendance records")
    
    # ==================== VISITORS ====================
    print("  Creating visitor records...")
    
    visitors_data = [
        ('Ahmed Khan', student_profiles[0], 'Family Visit'),
        ('Sana Ali', student_profiles[1], 'Friend Visit'),
        ('Imran Shah', student_profiles[2], 'Family Visit'),
        ('Nabeel Tariq', student_profiles[0], 'Cousin Visit'),
        ('Maria Ahmed', student_profiles[3], 'Sister Visit'),
        ('Kamran Malik', student_profiles[4], 'Father Visit'),
        ('Hina Iqbal', student_profiles[1], 'Mother Visit'),
        ('Asad Raza', student_profiles[2], 'Brother Visit'),
    ]
    
    for i, (name, student, purpose) in enumerate(visitors_data):
        in_time = datetime.now() - timedelta(hours=i*2)
        out_time = in_time + timedelta(hours=1) if i % 2 == 0 else None
        
        Visitor.objects.create(
            visitor_name=name,
            student=student,
            purpose=purpose,
            contact=f'0333{3000000 + i}',
            in_time=in_time,
            out_time=out_time,
            approved_by=warden
        )
    
    print(f"    ✓ Created {Visitor.objects.count()} visitor records")
    
    # ==================== COMPLAINTS ====================
    print("  Creating complaint records...")
    
    complaints_data = [
        ('Wi-Fi not working', 'Internet connection is very slow in room 102', Complaint.ELECTRICAL, Complaint.HIGH, Complaint.PENDING),
        ('AC not cooling', 'Air conditioner needs servicing', Complaint.MAINTENANCE, Complaint.MEDIUM, Complaint.IN_PROGRESS),
        ('Water leakage', 'Bathroom tap is leaking', Complaint.PLUMBING, Complaint.HIGH, Complaint.RESOLVED),
        ('Broken chair', 'Study chair is broken', Complaint.MAINTENANCE, Complaint.LOW, Complaint.RESOLVED),
        ('Room cleaning', 'Room needs thorough cleaning', Complaint.CLEANING, Complaint.MEDIUM, Complaint.PENDING),
        ('Light not working', 'Tube light in room is flickering', Complaint.ELECTRICAL, Complaint.MEDIUM, Complaint.IN_PROGRESS),
        ('Window broken', 'Window pane is cracked', Complaint.MAINTENANCE, Complaint.HIGH, Complaint.PENDING),
        ('Washroom issue', 'Flush is not working properly', Complaint.PLUMBING, Complaint.HIGH, Complaint.PENDING),
    ]
    
    for i, (title, desc, category, priority, status) in enumerate(complaints_data):
        complaint = Complaint.objects.create(
            student=student_profiles[i % len(student_profiles)],
            title=title,
            description=desc,
            category=category,
            priority=priority,
            status=status,
            resolved_by=warden if status == Complaint.RESOLVED else None,
            resolution_notes='Issue fixed' if status == Complaint.RESOLVED else ''
        )
    
    print(f"    ✓ Created {Complaint.objects.count()} complaint records")
    
    # ==================== MESS MENU ====================
    print("  Creating mess menu...")
    
    # Menu for next 7 days
    for i in range(7):
        menu_date = date.today() + timedelta(days=i)
        MessMenu.objects.create(
            date=menu_date,
            breakfast='Paratha, Egg, Tea, Bread, Butter',
            lunch='Rice, Chicken Curry, Roti, Salad, Raita',
            snacks='Samosa, Tea, Biscuits',
            dinner='Biryani, Raita, Salad' if i % 2 == 0 else 'Daal, Rice, Roti, Vegetables'
        )
    
    print(f"    ✓ Created {MessMenu.objects.count()} mess menu records")
    
    # ==================== CONTACT MESSAGES ====================
    print("  Creating contact messages...")
    
    contact_messages = [
        ('Ahmed Ali', 'ahmed@example.com', 'Student', 'How can I apply for hostel admission?'),
        ('Sara Khan', 'sara@example.com', 'Admin', 'Need help with fee payment system'),
        ('Usman Tariq', 'usman@example.com', 'Warden', 'Suggestion for mess improvement'),
    ]
    
    for name, email, role, message in contact_messages:
        ContactMessage.objects.create(
            name=name,
            email=email,
            role=role,
            message=message
        )
    
    print(f"    ✓ Created {ContactMessage.objects.count()} contact messages")
    
    # ==================== SUMMARY ====================
    print("\n✅ Seed data creation complete!")
    print(f"\n📊 Summary:")
    print(f"   Users: {User.objects.count()}")
    print(f"   Rooms: {Room.objects.count()}")
    print(f"   Students: {StudentProfile.objects.count()}")
    print(f"   Fees: {Fee.objects.count()}")
    print(f"   Attendance: {Attendance.objects.count()}")
    print(f"   Visitors: {Visitor.objects.count()}")
    print(f"   Complaints: {Complaint.objects.count()}")
    print(f"   Mess Menus: {MessMenu.objects.count()}")
    print(f"   Contact Messages: {ContactMessage.objects.count()}")
    
    print(f"\n🔑 Login Credentials:")
    print(f"   Admin:   username='admin'   password='admin123'")
    print(f"   Warden:  username='warden'  password='warden123'")
    print(f"   Student: username='ali_khan' password='student123'")
    print(f"            (or any other student username with password 'student123')")

if __name__ == '__main__':
    create_seed_data()
