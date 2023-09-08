from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

# Custom user model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=20)
    avatar = models.ImageField(default='user.png')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


# Group model
class Group(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    GROUP_TYPE_CHOICE = (
        (PUBLIC, 'public'),
        (PRIVATE, 'private')
    )

    group_name = models.CharField(max_length=20, null=False,blank=False)
    group_head = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='leader')
    description = models.TextField(null=True, blank=True)
    group_type = models.CharField(max_length=10,choices=GROUP_TYPE_CHOICE, default=PRIVATE)
    members = models.ManyToManyField(CustomUser, related_name='members')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=8, unique=True, help_text='Please enter a group code to join eg, ZATY123D')

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = 'group'
        ordering:['-updated_at', '-created_at']



# Task model
class Task(models.Model):
    task_name = models.CharField(max_length=30, null=False, blank=False)
    description = models.TextField(help_text="Enter the detail of the task in stepwise")
    assign_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    deadline = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)
    number_of_files = models.PositiveIntegerField(default=1)
    files_submitted = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_name

    class Meta:
        db_table = 'task'
        ordering:['-updated_at', '-created_at']


# Task files
class TaskFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files')
    file_name = models.CharField(max_length=100, null=True)
    file_extension = models.CharField(max_length=5, null=True)
    task_file = models.FileField(upload_to='task_files/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.file_name}'
    
    class Meta:
        db_table = 'task_file'



# Group message model
class GroupMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.body[0:10]

    class Meta:
        db_table = 'group_message'
        ordering: ['-updated_at', '-created_at']


class MessageReply(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group_message = models.ForeignKey(GroupMessage, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.body[0:10]

    class Meta:
        db_table = 'message_reply'
        ordering: ['-updated_at', '-created_at']

