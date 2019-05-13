from django.db import models

# Create your models here.

# User Database
class User(models.Model):
    user_id = models.CharField(max_length = 50, help_text = 'Enter User ID')
    password = models.CharField(max_length = 50, help_text = 'Enter password')
    user_name = models.CharField(max_length = 50, help_text = 'Enter user name')
    email = models.CharField(max_length = 100, help_text = 'Enter email')
    department = models.CharField(max_length = 50, help_text = 'Enter department')

    input_id = models.CharField(max_length = 50)
    input_ip = models.CharField(max_length = 15)
    input_data = models.DateTimeField()

    update_id = models.CharField(max_length = 50)
    update_ip = models.CharField(max_length = 15)
    update_data = models.DateTimeField()

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

# /DB 테이블 만들어 보려고 시도한 흔적임.

# class User(models.Model):
# 	db_id = models.CharField(max_length=45) # PK
# 	db_pwd = models.CharField(max_length=45)
# 	db_user_name = models.CharField(max_length=45)
# 	db_email = models.CharField(max_length=45)
# 	db_company = models.CharField(max_length=45) # IS NULL

# class File(models.Model):
# 	db_id = models.CharField(max_length=45) # FK
# 	db_fid = models.IntegerField(default=0) # PK
# 	db_path = models.CharField(max_length=200)

# class Result(models.Model):
# 	db_fid = models.IntegerField(default=0) # PK, FK
# 	db_result_fid = models.IntegerField(default=0) # PK, FK

# DB 테이블 만들어 보려고 시도한 흔적임./
