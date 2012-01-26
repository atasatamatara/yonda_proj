#-*- coding: utf-8 -*-
# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
#from django.shortcuts import get_object_or_404
#from django.core.mail import send_mail

from yonda.forms import *
from yonda.models import *

from BeautifulSoup import BeautifulSoup
import urllib2

def index(request):
    #loginしてるとき
    if request.method == "GET":
        return direct_to_template(request, "index.html", {"form":UrlPostForm()})
    if request.method == "POST":
        form = UrlPostForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect(reverse('index'))
        
        url = form.cleaned_data["url"]
        if "#!/" in url:
            url = url.replace("#!/","")
        #try:
        #    posted_user = User.objects.get(name=request.session["session_user"])
        #except:
        #    #TODO:増田
        #    posted_user = User.objects.get(pk=1)
        try:
            posted_user = request.session["session_user"]
        except:
            #TODO:増田
            posted_user = "増田"
        try:
            html = urllib2.urlopen(url).read()
            soup = BeautifulSoup(html)
            for s in soup('title'):
                souped_title = s.renderContents()
            decoded_title = souped_title.decode("utf-8")
            #import pdb;pdb.set_trace()
            url_count = Url.objects.filter(url=form.cleaned_data["url"]).filter(user=posted_user).count()
            #if Url.objects.filter(user=posted_user).count():
            url_count += 1
            url_instance = Url(url=form.cleaned_data["url"],
                               title=decoded_title,
                               user=posted_user,
                               count=url_count,
                               )
            url_instance.save()
        except:
            print 'error'
        return HttpResponseRedirect(reverse('index'))

#def signup(request):
#    if request.method == "GET":
#        return direct_to_template(request, 'signup.html',{'form':SingupFrom()})
#    if request.method == "POST":
#        form = SingupFrom(request.POST)
#        if not form.is_valid():
#            return HttpResponseRedirect(reverse('index'))
#        #存在しないユーザーならindexに戻す
#        #if not User.objects.filter(name=request.POST.get('name')).count():
#        #    return HttpResponseRedirect(reverse('index'))
#        new_user = User(name=form.cleaned_data["name"], 
#                        email=form.cleaned_data["email"])
#        new_user.save()
#        request.session['session_user'] = request.POST.get('name')
#        return HttpResponseRedirect(reverse('index'))

def login(request):
    if request.method == "GET":
        return direct_to_template(request, 'login.html',{'form':LoginForm()})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect(reverse('index'))
        if not User.objects.filter(name=request.POST.get('name')).count():
            new_user = User(name=form.cleaned_data["name"])
            new_user.save()
        request.session['session_user'] = request.POST.get('name')
        return HttpResponseRedirect(reverse('index'))

def logout(request):
    if request.session.get('session_user'):
        del request.session['session_user']
    return HttpResponseRedirect(reverse('index'))

def timeline(request):
    timeline = Url.objects.all().order_by('-ctime')
    return direct_to_template(request, "timeline.html",{'timeline':timeline})

def user_timeline(request, username):
    #user = User.objects.get(name=username)
    user_timeline = Url.objects.filter(user=username).order_by('-ctime')
    return direct_to_template(request,"user_timeline.html", {"user_timeline":user_timeline})

def bookmarklet(request):
    if request.method == "GET":
        #クエリからtitleとurlをとってくる
        title = request.GET.get('title')
        url = request.GET.get('url')
        #try:
        #    user = request.session["session_user"]
        #except:
        #    user = User.objects.get(pk=1)
        try:
            user = request.session["session_user"]
        except:
            #TODO:増田
            user = "増田"
        #bookmarkletなのでinitialをつける
        return direct_to_template(request, 'bookmarklet.html',{'form': BookmalkletForm(initial={'title':title,'url':url, 'user':user}) })
    #POSTの処理はbookmark_addと同じ
    if request.method == "POST":
        form = BookmalkletForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect(reverse('bookmarklet'))
        #import pdb;pdb.set_trace()
        #try:
        #    user = User.objects.get(name=request.session["session_user"])
        #except:
        #    user = User.objects.get(pk=1)
        try:
            posted_user = request.session["session_user"]
        except:
            #TODO:増田
            #posted_user = "増田"
            posted_user = request.POST.get("user")
        url_instance= Url(title=form.cleaned_data['title'],
                                user=posted_user,
                                url=form.cleaned_data['url'],
                               )
        url_instance.save()
        return HttpResponseRedirect(reverse('index'))
