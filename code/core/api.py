from ninja import NinjaAPI, Schema, Query
from django.db.models import Count
from pydantic import validator
import re
from typing import List
from django.urls import path
from core.schema import CourseFilter, DetailCourseOut
from ninja.responses import Response
from django.contrib.auth.models import User
from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from core.schema import CourseSchemaOut, CourseMemberOut, CourseSchemaIn, UserOut
from core.schema import CourseContentMini, CourseContentFull
from core.schema import CourseCommentOut, CourseCommentIn
from core.models import Course, CourseMember, CourseContent, Comment
from ninja.pagination import paginate, PageNumberPagination
from ninja.throttling import AnonRateThrottle, AuthRateThrottle

apiv1 = NinjaAPI(
    throttle=[
        AnonRateThrottle('10/s'), # Maksimum 10 permintaan per detik untuk pengguna anonim
        AuthRateThrottle('100/s'), # Maksimum 100 permintaan per detik untuk pengguna terautentikasi
    ],
)
apiv1.add_router("/auth/", mobile_auth_router)
apiAuth = HttpJwtAuth()

@apiv1.get('hello/')
def helloApi(request):
    return "Halo kawand..."

@apiv1.get('courses/', response=List[DetailCourseOut], auth=apiAuth)
@paginate(PageNumberPagination, page_size=10)
def listAllCourse(request, filters: CourseFilter=Query(...)):
    courses = Course.objects.all()
    courses = filters.filter(courses)
    
    # Annotate each course with the number of members and contents
    courses = courses.annotate(
        num_members=Count('coursemember'),
        num_contents=Count('coursecontent')
    )
    
    return courses

@apiv1.get("/courses", response=list[CourseSchemaOut])
@paginate(PageNumberPagination, page_size=10)
def list_courses(request):
    courses = Course.objects.select_related('teacher').all()
    return courses

# paginate list_users
@apiv1.get("/users", response=list[UserOut])
@paginate(PageNumberPagination, page_size=10)  # Untuk pagination jika banyak data
def get_users(request):
    users = User.objects.all()  # Mengambil semua data user
    return users


# - enroll course
@apiv1.post("/courses/{course_id}/enroll", auth=apiAuth, response=CourseMemberOut)
def enroll_course(request, course_id: int):
    user = User.objects.get(id=request.user.id)
    course = Course.objects.get(id=course_id)
    course_member = CourseMember(course_id=course, user_id=user, roles="std")
    course_member.save()
    # print(course_member)
    return course_member

# - my courses
@apiv1.get("/mycourses", auth=apiAuth, response=list[CourseMemberOut])
def my_courses(request):
    user = User.objects.get(id=request.user.id)
    courses = CourseMember.objects.select_related('user_id', 'course_id').filter(user_id=user)
    return courses

# - create content comment & throttling class
@apiv1.post("/contents/{content_id}/comments", auth=apiAuth, response={201: CourseCommentOut})
def create_content_comment(request, content_id: int, data: CourseCommentIn):
    user = User.objects.get(id=request.user.id)
    content = CourseContent.objects.get(id=content_id)

    if not content.course_id.is_member(user):
        message =  {"error": "You are not authorized to create comment in this content"}
        return Response(message, status=401)
    
    member = CourseMember.objects.get(course_id=content.course_id, user_id=user)
    
    comment = Comment(
        content_id=content,
        member_id=member,
        comment=data.comment
    )
    comment.save()
    return 201, comment

@apiv1.get('calc/{nil1}/{opr}/{nil2}')
def calculator(request, nil1:int, opr:str, nil2:int):
    hasil = nil1 + nil2
    if opr == '-':
        hasil = nil1 - nil2
    elif opr == 'x':
        hasil = nil1 * nil2
    
    return {'nilai1': nil1, 'nilai2': nil2, 'operator': opr, 'hasil': hasil}

@apiv1.post('hello/')
def helloPost(request):
    if 'nama' in request.POST:
        return f"Selamat menikmati ya {request.POST['nama']}"
    return "Selamat tinggal dan pergi lagi"

@apiv1.put('users/{id}')
def userUpdate(request, id:int):
    return f"User dengan id {id} Nama aslinya adalah Herdiono kemudian diganti menjadi {request.body}"

class Kalkulator(Schema):
    nil1: int
    nil2: int
    opr: str
    hasil: int = 0

    def calcHasil(self):
        if self.opr == '+':
            self.hasil = self.nil1 + self.nil2
        elif self.opr == '-':
            self.hasil = self.nil1 - self.nil2
        elif self.opr == 'x':
            self.hasil = self.nil1 * self.nil2
        else:
            self.hasil = 0
        return {
            'nilai1': self.nil1,
            'nilai2': self.nil2,
            'operator': self.opr,
            'hasil': self.hasil
        }
        
@apiv1.post('calc')
def postCalc(request, skim : Kalkulator):
    skim.hasil = skim.calcHasil()
    return skim

class Register(Schema):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str

    @validator("username")
    def validate_username(cls, value):
        if len(value) < 5:
            raise ValueError("Username harus lebih dari 5 karakter")
        return value

    @validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password harus lebih dari 8 karakter")
        pattern = r'^(?=.*[A-Za-z])(?=.*\d).+$'
        if not re.match(pattern, value):
            raise ValueError("Password harus mengandung huruf dan angka")
        return value
    
@apiv1.delete('users/{id}')
def userDelete(request, id:int):
    return f"Hapus user dengan id: {id}"

class UserOut(Schema):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str

@apiv1.post('register/', response=UserOut)
def register(request, data: Register):
    """
    Endpoint untuk registrasi pengguna dengan validasi:
    - username: minimal 5 karakter
    - password: minimal 8 karakter, harus mengandung huruf dan angka
    """
    new_user = User.objects.create_user(
        username=data.username,
        password=data.password,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
    )
    return new_user