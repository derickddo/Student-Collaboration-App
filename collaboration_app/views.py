from django.shortcuts import render, redirect, get_object_or_404
import string, secrets
from .models import Group, Task, GroupMessage, CustomUser, TaskFile, MessageReply
from .forms import GroupCreationForm, GroupJoiningForm, GroupMessageCreationForm, TaskCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
import requests
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings





# Create your views here.
def home(request):
    return render(request, 'collaboration_app/_home.html')

def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

def paraphrase_text(request):
    if request.method == 'POST':
        text = request.POST['text']

        url = "https://tinq.ai/api/v1/rewrite"

        payload = { "text": text}

        headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "authorization": "Bearer key-3f20f83c-9ff2-4990-9bcf-258733717ca2-64b18b84f237f"
        }

        response = requests.post(url, data=payload, headers=headers)
        print(response.text)

        rewritten_text = response.json()
        return JsonResponse({"rewritten_text": rewritten_text})
    


# private dashboard
@login_required(login_url='account_login')
def private_dashboard(request):
    if request.GET.get('search'):
        q = request.GET.get('search')
    else:
        q = ''
    user = request.user
    groups = Group.objects.filter(Q(group_type__icontains='private'), Q(group_name__icontains=q), Q(members__first_name__icontains=user.first_name))
    tasks = Task.objects.filter(assign_to=user)
    activities = GroupMessage.objects.filter(sender = user)
    context = {'groups':groups, 'tasks':tasks, 'activities':activities}

    return render(request, 'collaboration_app/dashboard.html', context)


# public dashboard
@login_required(login_url='account_login')
def public_dashboard(request):
    if request.GET.get('search'):
        q = request.GET.get('search')
    else:
        q = ''
    groups = Group.objects.filter(Q(group_type__icontains='public'), Q(group_name__icontains=q))
    context = {'groups':groups}
    
    return render(request, 'collaboration_app/public_dashboard.html', context)


# Code generation
def generate_code():
    code = string.ascii_uppercase + string.digits
    while True:
        generated_code = ''.join(secrets.choice(code) for i in range(8))
        if not Group.objects.filter(code=generated_code).exists():
            return generated_code

# Create a group
@login_required(login_url='account_login')
def create_group(request):
    form = GroupCreationForm()
    if request.method == 'POST':
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.group_head = request.user
            group.code = generate_code()
            group.save()
            group.members.add(group.group_head)
            
        return redirect('get_group', id=group.id)
    context = {'form':form}
    
    return render(request, 'collaboration_app/create_group.html', context)


# Join a group with group code for all types of groups
def join_group(request):
    user_id = request.user.id
    if request.POST.get('code'):
        code = request.POST.get('code') 
        group = Group.objects.get(code=code)

        context = {
            'group_head':group.group_head.first_name,
            'group_name':group.group_name,
            'user_name':request.user.first_name,
            'user_id':user_id,
            'group_id':group.pk,
        }

        if group.group_type == 'private':
            group_leader_email = group.group_head.email

            message = render_to_string('collaboration_app/emails/request_to_join_email.html',context)
        

            msg = EmailMessage(
                'Join Request', 
                message,
                settings.EMAIL_HOST_USER, 
                [group_leader_email],
            )
            msg.content_subtype = 'html'
            print(msg.body)
            msg.send(fail_silently=False)

            
        else:
            group.members.add(request.user)
        return redirect('dashboard')
   
    return render(request, 'collaboration_app/join_group.html')


# Join a group specifically public groups
def join_public_group(request, id):
    group = Group.objects.get(id=id)
    user_id = request.GET.get('user_id')
    user = CustomUser.objects.get(id=user_id)
    group.members.add(user)
    return redirect('get_group', id=id)


# join group request accepted
def accept_join_request(request,id):
    user = CustomUser.objects.get(id=id)
    if request.GET.get('q'):
        q = request.GET.get('q')
        group = Group.objects.get(id=q)
        group.members.add(user)
        group.save()
        user_email = user.email
        context = {
            'group_name':group.group_name,
            'user_name':request.user.first_name,
            'group_id':group.pk
        }
            
        message = render_to_string('collaboration_app/emails/accepted_request.html',context)
        msg = EmailMessage(
            'Accepted Request', 
            message, 
            settings.EMAIL_HOST_USER, 
            [user_email],  
        )
        msg.content_subtype = "html"
        msg.send(fail_silently=False)
    return redirect('get_group', id=group.pk) 
    

# Get a group
@login_required(login_url='account_login')
def get_group(request, id):
    group = Group.objects.get(id=id)
    members = group.members.all()
    tasks = group.task_set.all()
    activities = group.messages.all().order_by('-updated_at')
    task_files = TaskFile.objects.filter(task__in=tasks)

    if members.filter(id=request.user.id).exists():
        if request.method == 'POST':
            if request.POST.get('message'):
                data = request.POST.get('message')

                message = GroupMessage.objects.create(
                    body=data,
                    sender=request.user,
                    group=group,
                ) 
            else:
                reply_message = request.POST.get('reply')
                message_id = request.POST.get('message_id')
                message = GroupMessage.objects.get(id=message_id)
                reply = MessageReply.objects.create(
                    sender=request.user,
                    body=reply_message,
                    group_message=message
                )

        context = {
            'group':group, 
            'members':members, 
            'tasks':tasks, 
            'activities':activities,
            'task_files':task_files
        }

        return render(request, 'collaboration_app/get_group.html', context)
    else:
        return HttpResponse("Oops, Sorry you are not a member of this group!")

# remove member from group
def remove_member(request, id):
    group = Group.objects.get(id=id)
    q = request.GET.get('q')
    member = CustomUser.objects.get(id=q)
    if request.method == 'POST':
        group.members.remove(member)
        group.save()
        return redirect('get_group',id=id)
  
    return render(request, 'collaboration_app/delete.html', {'obj':member})

# create task
def create_task(request, id):
    form = TaskCreationForm()
    group = Group.objects.get(pk=id)
    members = group.members.all()
    if request.method == 'POST':
        form = TaskCreationForm(request.POST)
        deadline = request.POST.get('deadline')
        assign_to = request.POST.get('assign_to')
        user = get_object_or_404(CustomUser, id=assign_to)
        if form.is_valid():
            task = form.save(commit=False)
            task.group = group
            task.deadline = deadline
            task.assign_to = user
            task.save()
            return redirect('get_group', id=id)
    context = {'form':form, 'members':members}
    return render(request, 'collaboration_app/create_task.html', context)

# add member to group
def add_member(request, id):
    group = Group.objects.get(pk=id)
    if request.method == 'POST':
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.filter(email=email)
            print(user)
            group.members.add(user)
            group.save()
            return redirect('get_group', id=id)
        return HttpResponse("User not found")
    context = {}
    return render(request, 'collaboration_app/add_member.html', context)

# task details
@login_required(login_url='account_login')
def get_task(request, id):
    task = Task.objects.get(id=id)
    group = task.group
    task_files = task.files.all()
    group_leader = task.group.group_head
    
    if request.user == task.assign_to or request.user == group_leader:
        
        if request.FILES.get('file'):
            task_file = request.FILES.get('file')
            extension = str(task_file).split('.').pop(1)

            TaskFile.objects.create(
                task_file=task_file,
                task=task, 
                file_name=task_file.name, 
                file_extension=extension
            )

            task.files_submitted += 1
            task.save()
          
        # Calculations of the progress percentage 
        progress_percentage = task.files_submitted/ task.number_of_files * 100
        
        context = {
            'task':task,
            'task_files':task_files,
            'progress_percentage':int(progress_percentage), 
            'group':group,
        }
       
        return render(request, 'collaboration_app/get_task.html',context)

    else:
        return HttpResponse('Sorry, you can not access this task!')

    if request.method == 'POST':
        text = request.POST['text']

        url = "https://tinq.ai/api/v1/rewrite"

        payload = { "text": text}

        headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "authorization": "Bearer key-3f20f83c-9ff2-4990-9bcf-258733717ca2-64b18b84f237f"
        }

        response = requests.post(url, data=payload, headers=headers)
        print(response.text)

        rewritten_text = response.json()
        return JsonResponse({"rewritten_text": rewritten_text})

# delete a file from task
def delete_file(request, id):
    task_file = TaskFile.objects.get(id=id)
    q = request.GET.get('q')
    task = task_file.task
    if request.method == 'POST':
        task_file.delete()
        task.files_submitted -= 1
        task.save()
        return redirect('get_task', id=q)

    return render(request, 'collaboration_app/delete.html', {"obj":task_file})

# update group details
def update_group(request, id):
    url = request.path
    group = get_object_or_404(Group, id=id)
    if request.method == 'POST':
        form = GroupCreationForm(request.POST or None, instance=group)
        if form.is_valid():
            form.save()
            return redirect('get_group', id=id)
    context = {'form':form, 'url':url}
    return render(request, 'collaboration_app/create_group.html', context)

# delete group
def delete_group(request,id):
    group = get_object_or_404(Group, id=id)
    if request.method == 'POST':
        if request.user == group.group_head:
            group.delete()
            return redirect('home')
        else:
            return HttpResponse("You are not allowed to delete this group")
    return render(request, 'collaboration_app/delete.html', {"obj":group})

# update task
def update_task(request, id):
    url = request.path
    task = get_object_or_404(Task, id=id)
    form = TaskCreationForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('get_task', id=id)
    context = {'form':form, 'url':url}
    return render(request, 'collaboration_app/create_task.html', context)

def profile(request, id):
    user = CustomUser.objects.get(id=id)
    context = {'user':user}
    return render(request, 'collaboration_app/profile.html', context)