# Generated by Django 4.1 on 2022-08-22 19:42

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('ADMIN', 'Admin'), ('STUDENTS', 'Student'), ('TEACHER', 'Teacher')], max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('attendance_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('courses', models.CharField(max_length=250, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
                'ordering': ('courses',),
            },
        ),
        migrations.CreateModel(
            name='SessionYearModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('session_name', models.CharField(max_length=250)),
                ('session_start_year', models.DateField()),
                ('session_end_year', models.DateField()),
            ],
            options={
                'verbose_name': 'Session Year',
                'verbose_name_plural': 'Session Year Model',
                'ordering': ('session_start_year',),
            },
        ),
        migrations.CreateModel(
            name='Staffs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Staff',
                'verbose_name_plural': 'Staff',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=50)),
                ('profile_pics', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('address', models.TextField()),
                ('level', models.CharField(choices=[('ND1', 'ND1'), ('ND2', 'ND2'), ('HND1', 'HND1'), ('HND2', 'HND2')], max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.courses')),
                ('session_year_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.sessionyearmodel')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=250)),
                ('level', models.CharField(choices=[('ND1', 'ND1'), ('ND2', 'ND2'), ('HND1', 'HND1'), ('HND2', 'HND2')], max_length=200)),
                ('course', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.courses')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.staffs')),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
                'ordering': ('subject',),
            },
        ),
        migrations.CreateModel(
            name='StudentResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_exam_marks', models.FloatField(default=0)),
                ('subject_assignment_marks', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
                ('subject_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportStaff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_date', models.CharField(max_length=255)),
                ('leave_message', models.TextField()),
                ('leave_status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBackStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField()),
                ('feedback_reply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attendance_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.attendance')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.student')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='session_year_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.sessionyearmodel'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='subject_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.subjects'),
        ),
        migrations.CreateModel(
            name='AdminHod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Administrative',
                'verbose_name_plural': 'Administrative',
                'ordering': ('created_at',),
            },
        ),
    ]
