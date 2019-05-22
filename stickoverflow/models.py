from django.db import models

# Create your models here.

# User Database
class User(models.Model):
    user_id = models.CharField(max_length = 50, help_text = 'Enter User ID')
    password = models.CharField(max_length = 50, help_text = 'Enter password')
    user_name = models.CharField(max_length = 50, help_text = 'Enter user name')
    email = models.CharField(max_length = 100, help_text = 'Enter email')
    department = models.CharField(max_length = 50, help_text = 'Enter department', null = True)

    input_id = models.CharField(max_length = 50)
    input_ip = models.CharField(max_length = 15)
    input_data = models.DateTimeField(auto_now=True)

    update_id = models.CharField(max_length = 50)
    update_ip = models.CharField(max_length = 15)
    update_data = models.DateTimeField(auto_now=True)

    def check_password(self, password):
        return self.password == password

    def __str__(self):
        return self.user_id

# FILE Database
class File(models.Model):
    user_id = models.CharField(max_length = 50)
    file_no = models.IntegerField()
    file_name = models.CharField(max_length = 260)
    file_path = models.CharField(max_length = 260)
    file_description = models.CharField(max_length = 200)

# RESULT Database
class Result(models.Model):
    user_id = models.CharField(max_length = 50, help_text = 'Enter User ID')
    file_no = models.IntegerField()
    result_no = models.IntegerField()
    analysis_code = models.IntegerField()
    save_code = models.IntegerField()
