from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from main import models
from django.db.models import Sum
from datetime import date


def index(request):
    if request.method == 'GET':
        edu_center = request.user.education_center

        students = models.StudentModel.objects.filter(is_active=True, education_center=edu_center)
        teachers = models.StaffModel.objects.filter(is_active=True, education_center=edu_center, role='teacher')
        groups = models.GroupInfoModel.objects.filter(is_active=True, education_center=edu_center)

        today = date.today()
        payments = models.PaymentModel.objects.filter(
            is_active=True,
            education_center=edu_center,
            paid_at=today
        )
        total_paid_today = payments.aggregate(total=Sum('amount'))['total'] or 0

        context = {
            'students': len(students),
            'teachers': len(teachers),
            'groups': len(groups),
            'total_paid_today': total_paid_today
        }
        return render(request, 'index.html', context=context)