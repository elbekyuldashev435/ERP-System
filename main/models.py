from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    @classmethod
    def all(cls):
        return cls.objects.filter(is_active=True)


class EduModel(BaseModel):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='edu_logo/', null=True, blank=True)

    @property
    def staff_count(self):
        return StaffModel.objects.filter(education_center=self, is_active=True).count()

    class Meta:
        verbose_name = 'Markaz'
        verbose_name_plural = 'Markazlar'


class User(AbstractUser):
    education_center = models.ForeignKey(EduModel, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class SubscriptionModel(BaseModel):
    education_center = models.ForeignKey(EduModel, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duration = models.IntegerField(default=0)
    staff_quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Obuna xizmati'
        verbose_name_plural = 'Obuna xizmatlari'


#########################################################################################################
# XODIMLAR
#########################################################################################################


class SpecialityModel(BaseModel):
    name = models.CharField(max_length=100)
    education_center = models.ForeignKey(EduModel, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"mutaxasislik: {self.name}"

    class Meta:
        verbose_name = "Xodim mutaxasisligi"
        verbose_name_plural = "Xodimlar mutaxasisliglari"


class StaffModel(BaseModel):
    education_center = models.ForeignKey(EduModel, on_delete=models.SET_NULL, blank=True, null=True)
    class RoleChoices(models.TextChoices):
        TEACHER = 'teacher', 'Teacher'
        ADMIN = 'admin', 'Admin'
        MANAGER = 'manager', 'Manager'

    profile = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    phone_number = models.CharField(max_length=13)
    avatar = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gender = models.CharField(max_length=100, choices=[('MALE', 'Erkak'), ('FEMALE', 'Ayol')], blank=True, null=True)
    experience = models.PositiveIntegerField()
    role = models.CharField(max_length=20, choices=RoleChoices.choices)
    staff_speciality = models.ForeignKey(SpecialityModel, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    salary = models.IntegerField(
        choices=(
            (1, 'monthly'),
            (2, 'workly'),
            (3, 'daily'),

        )
    )
    salary_amount = models.DecimalField(max_digits=25, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.profile.first_name} {self.profile.last_name}'

    class Meta:
        verbose_name = 'Xodim'
        verbose_name_plural = 'Xodimlar'


class MakeStaffSalary(BaseModel):
    staff = models.ForeignKey(StaffModel, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=25, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_active == False:
            self.staff.balance -= self.amount

        else:
            if not self.id:
                self.staff.balance += self.amount
            else:
                old_instance = MakeStaffSalary.objects.get(id=self.id)
                difference = self.amount - old_instance.amount
                self.staff.balance += difference

        self.staff.save()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Maosh tayinlash'
        verbose_name_plural = 'Maoshlar tayinlash'


class GiveStaffSalary(BaseModel):
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=25, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    payment_type = models.ForeignKey("PaymentTypeModel", on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_active == False:
            self.staff.balance += self.amount
        else:
            if not self.id:
                self.staff.balance -= self.amount
            else:
                old_instance = GiveStaffSalary.objects.get(id=self.id)
                difference = self.amount - old_instance.amount
                self.staff.balance += difference

        self.staff.save()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Maosh berish'
        verbose_name_plural = 'Maosh berishlar'


class StaffFine(BaseModel):
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=25, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_active == False:
            self.staff.balance += self.amount
        else:
            if not self.id:
                self.staff.balance -= self.amount
            else:
                old_instance = StaffFine.objects.get(id=self.id)
                difference = self.amount - old_instance.amount
                self.staff.balance += difference

        self.staff.save()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Xodim qarz'
        verbose_name_plural = 'Xodim qarzlar'


#########################################################################################################
# O'QUVCHILAR
#########################################################################################################


class StudentModel(BaseModel):

    education_center = models.ManyToManyField(EduModel)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    third_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    data_birth = models.DateField()
    bio = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'O‘quvchi'
        verbose_name_plural = 'O‘quvchilar'


#########################################################################################################
# GURUX MALUMOTLAR
#########################################################################################################


class GroupInfoModel(BaseModel):
    education_center = models.ForeignKey(EduModel, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(StaffModel, on_delete=models.PROTECT)
    start_time = models.DateField()
    end_time = models.DateField()
    price = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Guruh ma’lumoti'
        verbose_name_plural = 'Guruhlar ma’lumotlari'


class GroupModel(BaseModel):
    created = models.DateTimeField(auto_now_add=True)
    group_info = models.ForeignKey(GroupInfoModel, on_delete=models.PROTECT)
    student = models.ForeignKey(StudentModel, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.group_info.name} {self.student.first_name}"

    class Meta:
        verbose_name = 'Guruh a’zosi'
        verbose_name_plural = 'Guruhdagi o‘quvchilar'


class ScheduleModel(BaseModel):
    group = models.ForeignKey(GroupInfoModel, on_delete=models.PROTECT, related_name='schedule')
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('monday', 'Dushanba'),
            ('tuesday', 'Seshanba'),
            ('wednesday', 'Chorshanba'),
            ('thursday', 'Payshanba'),
            ('friday', 'Juma'),
            ('saturday', 'Shanba'),
            ('sunday', 'Yakshanba'),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('group', 'day_of_week')
        verbose_name = 'Dars kuni'
        verbose_name_plural = 'Dars kunlari'

    def __str__(self):
        return f"{self.group} - {self.day_of_week.capitalize()} ({self.start_time}-{self.end_time})"


#########################################################################################################
# TO'LOV QISM
#########################################################################################################


class PaymentModel(BaseModel):
    education_center = models.ForeignKey(EduModel, on_delete=models.SET_NULL, blank=True, null=True)
    student = models.ForeignKey(StudentModel, on_delete=models.PROTECT)
    payment_type = models.ForeignKey('PaymentTypeModel', on_delete=models.SET_NULL, blank=True, null=True)
    group = models.ForeignKey(GroupModel, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.amount}"

    class Meta:
        verbose_name = 'To‘lov'
        verbose_name_plural = 'To‘lovlar'


class PaymentTypeModel(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'To\'lov turi'
        verbose_name_plural = 'To\'lov turlari'


#########################################################################################################
# DARS, VAZIFA VA IMTIXON
#########################################################################################################


class LessonPlanModel(BaseModel):
    group = models.ForeignKey(GroupInfoModel, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    lesson_number = models.PositiveIntegerField()
    scheduled_date = models.DateField()

    class Meta:
        unique_together = ('group', 'lesson_number')
        ordering = ['lesson_number']
        verbose_name = 'Dars rejasi'
        verbose_name_plural = 'Dars rejalari'

    def __str__(self):
        return f"{self.group} - Dars {self.lesson_number}"


class HomeworkModel(BaseModel):
    created = models.DateTimeField(auto_now_add=True)
    lesson = models.ForeignKey(LessonPlanModel, on_delete=models.PROTECT)
    teacher = models.ForeignKey(StaffModel, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    attachment = models.FileField(
        upload_to='media/homework_attachments/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=[
                'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt'
            ])
        ],
        help_text="PDF, Word hujjat yoki rasm yuklashingiz mumkin. Majburiy emas."
    )

    def __str__(self):
        return f"{self.lesson} - {self.title}"

    class Meta:
        verbose_name = 'Uyga vazifa'
        verbose_name_plural = 'Uyga vazifalar'


class StudentHomeworkModel(BaseModel):
    homework = models.ForeignKey(HomeworkModel, on_delete=models.PROTECT)
    student = models.ForeignKey(StudentModel, on_delete=models.PROTECT)
    submitted_text = models.TextField(blank=True, null=True)
    submitted_file = models.FileField(
        upload_to='media/homeworks/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'jpeg', 'png'])]
    )
    submitted_at = models.DateTimeField(blank=True, null=True)
    mark = models.PositiveSmallIntegerField(blank=True, null=True)  # 1-5
    teacher_comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('homework', 'student')
        verbose_name = 'Topshirilgan vazifa'
        verbose_name_plural = 'Topshirilgan vazifalar'

    def clean(self):
        if self.mark is not None and (self.mark < 1 or self.mark > 5):
            raise ValidationError("Baho 1 dan 5 gacha bo'lishi kerak.")

    def save(self, *args, **kwargs):
        if (self.submitted_text or self.submitted_file) and not self.submitted_at:
            self.submitted_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        status = "Topshirildi" if self.submitted_at else "Topshirilmagan"
        return f"{self.student} - {self.homework.title} - {status}"


#########################################################################################################
# DAVOMAT
#########################################################################################################


class AttendanceModel(BaseModel):
    lesson = models.ForeignKey(LessonPlanModel, on_delete=models.PROTECT)
    student = models.ForeignKey(StudentModel, on_delete=models.PROTECT)
    is_present = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('lesson', 'student')
        verbose_name = 'Davomat'
        verbose_name_plural = 'Davomatlar'

    def __str__(self):
        return f"{self.lesson} - {self.student} - {'Bordi' if self.is_present else 'Kelmagan'}"