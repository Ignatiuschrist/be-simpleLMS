from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
# from django.db.models import Count, Min, Max, Avg
from core.models import Course
from django.core import serializers
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return HttpResponse("<h1>be simple_lms</h1>")

def testing(request):
    dataCourse = Course.objects.all()
    dataCourse = serializers.serialize("python", dataCourse)
    return JsonResponse(dataCourse, safe=False)

def addData(request):
    course = Course(
        name = "Belajar Django",
        description = "Belajar Django dengan Mudah",
        price = 1000000,
        teacher = User.objects.get(username="admin")
    )
    course.save()
    return JsonResponse({"message": "Data berhasil ditambahkan"})

def editData(request):
    course = Course.objects.filter(name="Belajar Django").first()
    course.name = "Belajar Django Setelah update"
    course.save()
    return JsonResponse({"message": "Data berhasil diubah"})

def deleteData(request):
    course = Course.objects.filter(name__icontains="Belajar Django").first()
    course.delete()
    return JsonResponse({"message": "Data berhasil dihapus"})

# def allCourses(request):
#     courses = Course.objects.all().select_related('teacher')
#     data_resp = []
#     for course in courses:
#         record = {'id': course.id, 'name': course.name,
#                   'price': course.price,
#                   'teacher': {
#                       'id' : course.teacher.id,
#                       'username': course.teacher.username,
#                       'email': course.teacher.email,
#                       'fullname': f"{course.teacher.first_name} {course.teacher.last_name}"
#                   }}
#         data_resp.append(record)
        
#     return JsonResponse(data_resp, safe=False)
    
# def userProfile(request, user_id):
#     user = User.objects.get(pk=user_id)
#     courses = Course.objects.filter(teacher=user)
#     data_resp = {'username': user.username, 'email': user.email,
#                  'fullname': f"{user.first_name} {user.last_name}"}
#     data_resp['courses'] = []
#     for course in courses:
#         course_data = {'id': course.id, 'name': course.name, 'description': course.description,
#                        'price': course.price}
#         data_resp['courses'].append(course_data)
    
#     return JsonResponse(data_resp, safe=False)

# def courseStats(request):
#     courses = Course.objects.all()
#     statistic = courses.aggregate(course_count=Count('*'),
#                                   min_price=Min('price'),
#                                   max_price=Max('price'),
#                                   avg_price=Avg('price'))
#     cheapest_list = Course.objects.filter(price=statistic['min_price'])
#     expensive_list = Course.objects.filter(price=statistic['max_price'])
#     popular_list = Course.objects.annotate(member_count=Count('coursemember'))\
#                                  .order_by('-member_count')[:3]
#     unpopular_list = Course.objects.annotate(member_count=Count('coursemember'))\
#                                    .order_by('member_count')[:3]

#     data_resp = {
#         'course_count': statistic['course_count'],
#         'min_price': statistic['min_price'],
#         'max_price': statistic['max_price'],
#         'avg_price': statistic['avg_price'],
#         'cheapest': [course.name for course in cheapest_list],
#         'expensive': [course.name for course in expensive_list],
#         'popular': [course.name for course in popular_list],
#         'unpopular': [course.name for course in unpopular_list],
#     }
    
#     return JsonResponse(data_resp, safe=False)

# def courseDetail(request, course_id):
#     course = Course.objects.annotate(member_count=Count('coursemember'), 
#                                      content_count=Count('coursecontent'),
#                                      comment_count=Count('coursecontent__comment'))\
#                            .get(pk=course_id)
#     contents = CourseContent.objects.filter(course_id=course.id)\
#                .annotate(count_comment=Count('comment'))\
#                .order_by('-count_comment')[:3]
    
#     data_resp = {
#         "name": course.name,
#         'description': course.description,
#         'price': course.price, 
#         'member_count': course.member_count,
#         'content_count': course.content_count,
#         'teacher': {
#             'username': course.teacher.username,
#             'email': course.teacher.email,
#             'fullname': f"{course.teacher.first_name} {course.teacher.last_name}"
#         },
#         'comment_stat': {
#             'comment_count': course.comment_count, 
#             'most_comment': [
#                 {'name': content.name, 'comment_count': content.count_comment} 
#                 for content in contents
#             ]
#         },
#     }
    
#     return JsonResponse(data_resp, safe=False)
