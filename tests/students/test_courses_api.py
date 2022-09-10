import pytest
from model_bakery import baker

from students.models import Course, Student
from rest_framework.test import APIClient


# def test_example():
#     assert False, "Just test example"


@pytest.fixture
def apicle():
    return APIClient()


@pytest.fixture
def create_course():
    def create(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return create


@pytest.fixture
def student():
    def create(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return create


@pytest.mark.django_db
def test_course_one(apicle, create_course):
    course = create_course(_quantity=1)
    response = apicle.get('/api/v1/courses/1/')
    assert response.status_code == 200
    data = response.json()
    assert course[0].name == data['name']


@pytest.mark.django_db
def test_course_list(apicle, create_course):
    courses = create_course(_quantity=5)
    response = apicle.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    for d in data:
        count = 0
        if d['id']:
            count += 1
        if count > 0:
            assert True
            break


@pytest.mark.django_db
def test_course_filt_id(apicle, create_course):
    courses = create_course(_quantity=5)
    response = apicle.get(f'/api/v1/courses/?id={courses[2].id}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == courses[2].id


@pytest.mark.django_db
def test_course_filt_name(apicle, create_course):
    courses = create_course(_quantity=5)
    response = apicle.get(f'/api/v1/courses/?name={courses[2].name}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[2].name


@pytest.mark.django_db
def test_course_create(apicle):
    response = apicle.post('/api/v1/courses/', {'name': 'rat'}, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_course_patch(apicle, create_course):
    course = create_course(_quantity=1)
    response = apicle.patch(f'/api/v1/courses/{course[0].id}/', {'name': 'rat'}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_course_del(apicle, create_course):
    course = create_course(_quantity=1)
    response = apicle.delete(f'/api/v1/courses/{course[0].id}/')
    assert response.status_code == 204
