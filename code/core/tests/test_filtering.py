from django.test import TestCase
from models import Course
from datetime import datetime

class CourseFilterTest(TestCase):
    def setUp(self):
        # Menyiapkan data untuk pengujian
        self.course1 = Course.objects.create(name="Course 1", price=100, created_at=datetime(2023, 1, 1))
        self.course2 = Course.objects.create(name="Course 2", price=200, created_at=datetime(2023, 2, 1))
        self.course3 = Course.objects.create(name="Course 3", price=300, created_at=datetime(2023, 3, 1))

    def test_filter_price_gte(self):
        filters = {"price_gte": 150}
        response = self.client.get("/api/v1/courses/", data=filters)

        # Memeriksa bahwa hanya course dengan harga >= 150 yang dikembalikan
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.course2, response.context['courses'])
        self.assertIn(self.course3, response.context['courses'])
        self.assertNotIn(self.course1, response.context['courses'])

    def test_filter_price_lte(self):
        filters = {"price_lte": 150}
        response = self.client.get("/api/v1/courses/", data=filters)

        # Memeriksa bahwa hanya course dengan harga <= 150 yang dikembalikan
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.course1, response.context['courses'])
        self.assertNotIn(self.course2, response.context['courses'])
        self.assertNotIn(self.course3, response.context['courses'])

# berdasarkan tanggal

    def test_filter_created_gte(self):
        filters = {"created_gte": "2023-02-01"}
        response = self.client.get("/api/v1/courses/", data=filters)

        # Memeriksa bahwa hanya course yang dibuat pada atau setelah 2023-02-01 yang dikembalikan
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.course2, response.context['courses'])
        self.assertIn(self.course3, response.context['courses'])
        self.assertNotIn(self.course1, response.context['courses'])

    def test_filter_created_lte(self):
        filters = {"created_lte": "2023-02-01"}
        response = self.client.get("/api/v1/courses/", data=filters)

        # Memeriksa bahwa hanya course yang dibuat pada atau sebelum 2023-02-01 yang dikembalikan
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.course1, response.context['courses'])
        self.assertNotIn(self.course2, response.context['courses'])
        self.assertNotIn(self.course3, response.context['courses'])

# berdasarkan pencarian

    def test_filter_search(self):
        filters = {"search": "Course 1"}
        response = self.client.get("/api/v1/courses/", data=filters)

        # Memeriksa bahwa hanya course yang berisi "Course 1" dalam nama atau deskripsi yang dikembalikan
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.course1, response.context['courses'])
        self.assertNotIn(self.course2, response.context['courses'])
        self.assertNotIn(self.course3, response.context['courses'])
