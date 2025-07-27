from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from uuid import UUID
from main import models


def student_list(request):
    students = models.StudentModel.objects.filter(education_center=request.user.education_center)
    context = {
        'students': students
    }

    return render(request, 'student/student_list.html', context=context)