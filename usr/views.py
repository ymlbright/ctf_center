from django.http import HttpResponse,HttpResponseRedirect
#from django.template import Template,Context
#from django.template.loader import get_template
from django.shortcuts import render_to_response,RequestContext
from django.utils import simplejson
from django.core.urlresolvers import reverse  
# Create your views here.
from usr.models import User,Notice
#from usr.template import *
from usr.questionviews import question_view,question_detial,solve_question
import hashlib
from time import time

def index(request):
	
	return render_to_response('index.html',locals())

def scoreboard(request):
	q = {'nav1':'active'}
	try:
		q['score'] = User.objects.order_by('-score').filter(score__gt=0)[:30]
		return render_to_response('scoreboard.html',locals());
	except:
		q['error'] = 'database error'
		return render_to_response('error.html',locals())

def question(request,type):
	try:
		page = request.GET['page']
	except:
		page = 1
	q = question_view(type,request.session.get('uid',0),page)
	if q['error']:
		return render_to_response('error.html',locals())
	else:
		return render_to_response('question.html',locals())

def detial(request,id):
	q = question_detial(id,request.session.get('uid',0))
	if q['error']:
		return render_to_response('error.html',locals())
	else:
		return render_to_response('detial.html',locals(),context_instance=RequestContext(request))

def notice(request):
	q = {'nav8':'active'}
	try:
		q['notice'] = Notice.objects.order_by('-date').all()
	except:
		q['error'] = 'database error'
		return render_to_response('error.html',locals())
	return render_to_response('notice.html',locals())

def myscore(request):
	q = {'nav1':'active'}
	if request.session.get('uid'):
		if 1:
			u = User.objects.get(uid=request.session['uid'])
			n = User.objects.order_by('-score').filter(score__gte=u.score).count()
			q['myindex'] = n
			if n<11:
				n=0
			else:
				n=n-16
			q['myscore'] = User.objects.order_by('-score').filter(score__gte=0)[n:n+30]
			i = 1
			for m in q['myscore']:
				setattr(m,'index',n+i)
				i = i + 1
			return render_to_response('scoreboard.html',locals())
		try:
			pass
		except:
			q['error'] = 'database error'
			return render_to_response('error.html',locals())
	return render_to_response('scoreboard.html',locals())

def signin(request):
	return render_to_response('signin.html',locals(),context_instance=RequestContext(request))

def login(request):
	if request.method == 'POST' and 'user' in request.POST and 'pwd' in request.POST:
		data = {'status':0}
		data['msg'] = 'Username or password wrong.'
		try:
			u = User.objects.get(name=request.POST['user'])
		except:
			return HttpResponse(simplejson.dumps(data, ensure_ascii=False))
		r = u.login(request.POST['pwd'],request.META['REMOTE_ADDR'])
		if r == 1:
			request.session['uid'] = u.uid
			request.session['username'] = u.name
			data['jump'] = reverse('usr.views.index')
			data['status'] = 1
		elif r == -1:
			data['status'] = r
			data['msg'] = 'Your account had been locked or your email has\'t authenticate.'
		return HttpResponse(simplejson.dumps(data, ensure_ascii=False))
	else:
		return HttpResponse('')

def logout(request):
	try:
		del request.session['uid']
		del request.session['username']
	except:
		pass
	return HttpResponseRedirect(reverse('usr.views.index'))

def reg(request):
	if request.method == 'POST' and 'user' in request.POST and 'pwd' in request.POST and 'email' in request.POST :
		data = {'status':-1}
		try:
			x = User.objects.get(name=request.POST['user'])
		except:
			data['status']=0
			try:
				u = User.objects.create(
					name=request.POST['user'],
					pwd=hashlib.sha1(request.POST['pwd']).hexdigest(),
					email=request.POST['email'],status='1')
			except:
				return HttpResponse(simplejson.dumps(data, ensure_ascii=False))
			data['jump'] = reverse('usr.views.signin')
			data['status'] = 1
		return HttpResponse(simplejson.dumps(data, ensure_ascii=False))
	else:
		return HttpResponse('')

def register(request):
	return render_to_response('register.html',locals(),context_instance=RequestContext(request))

def flag(request):
	if request.method == 'POST' and 'flag' in request.POST and 'qid' in request.POST:
		if request.session.get('uid'):
			return HttpResponse(simplejson.dumps(solve_question(request.POST['qid'],
				request.session['uid'],request.POST['flag']), ensure_ascii=False))
		else:
			return HttpResponse(simplejson.dumps({'status':0,'msg':'Please sign in first.'}, ensure_ascii=False))
	else:
		return HttpResponse('')