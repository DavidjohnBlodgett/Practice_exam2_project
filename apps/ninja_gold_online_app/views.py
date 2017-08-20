from django.shortcuts import render, HttpResponse, redirect
from .models import User, Activity
from django.contrib import messages
from random import randint

def index(request):
    return render(request, 'ninja_gold_online_app/index.html')

def create(request):
    if User.objects.create_user(request):
        return redirect('/dashboard/')
    else:
        return redirect('/')

def login(request):
    if User.objects.login_user(request):
        return redirect('/dashboard/')
    else:
        return redirect('/')

def dashboard(request):
    context = {'topFive': User.objects.all().order_by('-gold')[:5]}
    return render(request, 'ninja_gold_online_app/dashboard.html', context)

def play(request):
    context = {'gold': User.objects.get(id=request.session['id']).gold, 'activities': Activity.objects.filter(user=request.session['id'])}
    return render(request, 'ninja_gold_online_app/play.html', context)

def show(request):
    context = {'all_users': User.objects.all()}
    return render(request, 'ninja_gold_online_app/all_users.html', context)

def showOne(request, user_id):
    context = {'user': User.objects.get(id=user_id), 'activities': Activity.objects.filter(user=user_id)}
    return render(request, 'ninja_gold_online_app/user.html', context)

def update(request):
    user = User.objects.get(id=request.session['id'])
    if request.POST['action'] == 'cave':
        reward = randint(-5, 5)
        print 'cave'
        print(reward)
        log_string = '{0} found {1} gold in the {2}'.format(user.name,reward,request.POST['action'])
        user.gold = user.gold + reward
    if request.POST['action'] == 'castle':
        reward = randint(-10, 10)
        print 'castle'
        print(reward)
        log_string = '{0} found {1} gold in the {2}'.format(user.name,reward,request.POST['action'])
        user.gold = user.gold + reward
    if request.POST['action'] == 'farm':
        reward = randint(-1, 1)
        print 'farm'
        print(reward)
        log_string = '{0} found {1} gold in the {2}'.format(user.name,reward,request.POST['action'])
        user.gold = user.gold + reward

    # generate an activity
    log = Activity.objects.create(content=log_string,user=user)

    # save state...
    log.save()
    user.save()

    # add log_string to session to print on play screen...
    if 'logs' in request.session:
        request.session['logs'].append(log_string)
    else:
        request.session['logs'] = []
        request.session['logs'].append(log_string)

    # if failed state delete user...
    if user.gold < 0:
        messages.error(request, 'Your broke!', extra_tags='broke')
        return redirect('/users/{0}/delete'.format(user.id))
    else:
        return redirect('/play/')

def logout(request):
    request.session.flush()
    return redirect('/')

def delete(request, user_id):
    User.objects.get(id=request.session['id']).delete()
    request.session.flush()
    return HttpResponse('You\'ve been deleted!!!')
