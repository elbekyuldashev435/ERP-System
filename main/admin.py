from django.contrib import admin
from . import models


@admin.register(models.SpecialityModel)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(models.StaffModel)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'role')


@admin.register(models.StudentModel)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'first_name', 'last_name', 'phone_number', 'data_birth')
    search_fields = ('first_name', 'last_name', 'phone_number')
    ordering = ('last_name',)


@admin.register(models.GroupInfoModel)
class GroupInfoAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'teacher', 'start_time', 'end_time', 'price')
    search_fields = ('name', 'teacher__first_name', 'teacher__last_name')
    ordering = ('name',)


@admin.register(models.GroupModel)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'group_info', 'student', 'created')
    search_fields = ('group_info__name', 'student__first_name', 'student__last_name')
    ordering = ('-created',)


@admin.register(models.ScheduleModel)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'group', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)
    ordering = ('group', 'day_of_week')


@admin.register(models.PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'student', 'group', 'amount', 'paid_at')
    list_filter = ('paid_at',)
    search_fields = ('student__first_name', 'student__last_name')
    ordering = ('-paid_at',)


@admin.register(models.LessonPlanModel)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'group', 'lesson_number', 'title', 'scheduled_date')
    ordering = ('group', 'lesson_number')


@admin.register(models.HomeworkModel)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'lesson', 'title', 'teacher', 'start_time', 'end_time')
    search_fields = ('title',)
    ordering = ('-created',)


@admin.register(models.StudentHomeworkModel)
class StudentHomeworkAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'homework', 'student', 'submitted_at', 'mark')
    list_filter = ('mark', 'submitted_at')
    search_fields = ('student__first_name', 'homework__title')


@admin.register(models.AttendanceModel)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'student', 'is_present', 'created')
    list_filter = ('is_present', 'created')
    search_fields = ('student__first_name', 'lesson__title')


@admin.register(models.EduModel)
class EduAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'phone')
    search_fields = ('name', 'phone')
    ordering = ('name',)


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'education_center', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'education_center')
    ordering = ('username',)


@admin.register(models.SubscriptionModel)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'staff_quantity', 'created')
    search_fields = ('name',)
    list_filter = ('created',)
    ordering = ('-created',)


@admin.register(models.MakeStaffSalary)
class MakeStaffSalaryAdmin(admin.ModelAdmin):
    list_display = ('staff', 'amount', 'date', 'description', 'is_active')
    search_fields = ('staff__first_name', 'staff__last_name')
    list_filter = ('date', 'is_active')
    ordering = ('-date',)


@admin.register(models.GiveStaffSalary)
class GiveStaffSalaryAdmin(admin.ModelAdmin):
    list_display = ('staff', 'amount', 'date', 'payment_type', 'is_active')
    search_fields = ('staff__first_name', 'staff__last_name')
    list_filter = ('date', 'payment_type', 'is_active')
    ordering = ('-date',)


@admin.register(models.StaffFine)
class StaffFineAdmin(admin.ModelAdmin):
    list_display = ('staff', 'amount', 'date', 'description', 'is_active')
    search_fields = ('staff__first_name', 'staff__last_name')
    list_filter = ('date', 'is_active')
    ordering = ('-date',)


@admin.register(models.PaymentTypeModel)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
