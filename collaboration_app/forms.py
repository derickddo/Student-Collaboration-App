from django.forms import ModelForm
from allauth.account.forms import SignupForm
from .models import CustomUser, Group, Task, GroupMessage
from django import forms


class UserCreationForm(SignupForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'password1']

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class GroupCreationForm(ModelForm):
    class Meta:
        model = Group
        fields = ['group_name', 'description', 'group_type']

class GroupJoiningForm(ModelForm):
    class Meta:
        model = Group
        fields = ['code']


class TaskCreationForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'description', 'number_of_files']


class GroupMessageCreationForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']




    