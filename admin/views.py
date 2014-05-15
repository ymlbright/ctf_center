from django.http import HttpResponse,HttpResponseRedirect
#from django.template import Template,Context
#from django.template.loader import get_template
from django.shortcuts import render_to_response,RequestContext
from django.utils import simplejson
from django.core.urlresolvers import reverse  
from django.core.paginator import Paginator
# Create your views here.
from usr.models import User,Question,Notice
from time import time

def signin(request):
	if request.session.get('auth'):
		return render_to_response('admin/index.html',locals())
	else:
		return render_to_response('admin/signin.html',locals(),context_instance=RequestContext(request))

def login(request):
	if 'user' in request.POST and 'pwd' in request.POST:
		if request.POST['user'] == 'admin' and request.POST['pwd'] == 'bright':
			request.session['auth'] = True
			return HttpResponse(simplejson.dumps({'status':'1','jump':reverse('admin.views.signin')}, ensure_ascii=False))
		else:
			return HttpResponse(simplejson.dumps({'status':'0'}, ensure_ascii=False))
	else:
		return HttpResponse('')

def logout(request):
	try:
		del request.session['auth']
	except:
		pass
	return HttpResponseRedirect(reverse('usr.views.index'))

def user(request):
	if request.session.get('auth'):
		q = {'nav1':'active'}
		try:
			page = request.GET['page']
		except:
			page = 1
		paginator =  Paginator(User.objects.all(),50)
		q['user'] = paginator.page(page)
		q['pagenow'] = page
		q['pageall'] = paginator.num_pages
		q['pagepre'] = int(page) - 1
		q['pagenex'] = int(page) + 1
		return render_to_response('admin/user.html',locals())
	else:
		return render_to_response('admin/signin.html',locals(),context_instance=RequestContext(request))

def question(request):
	if request.session.get('auth'):
		q = {'nav2':'active'}
		try:
			page = request.GET['page']
		except:
			page = 1
		paginator =  Paginator(Question.objects.all(),50)
		q['q'] = paginator.page(page)
		q['pagenow'] = page
		q['pageall'] = paginator.num_pages
		q['pagepre'] = int(page) - 1
		q['pagenex'] = int(page) + 1
		return render_to_response('admin/question.html',locals())
	else:
		return render_to_response('admin/signin.html',locals(),context_instance=RequestContext(request))

def notice(request):
	if request.session.get('auth'):
		q = {'nav3':'active'}
		q['n'] = Notice.objects.order_by('-nid').all()
		return render_to_response('admin/notice.html',locals())
	else:
		return render_to_response('admin/signin.html',locals(),context_instance=RequestContext(request))

def notice_add(request):
	if request.session.get('auth'):
		q = {'nav3':'active'}
		if 'notice' in request.POST:
			try:
				Notice.objects.create(date=time(),content=request.POST['notice'])
				return HttpResponse(simplejson.dumps({'status':1,'jump':reverse('admin.views.notice')}, ensure_ascii=False))
			except:
				return HttpResponse(simplejson.dumps({'status':0}, ensure_ascii=False))
		else:
			return render_to_response('admin/notice_add.html',locals(),context_instance=RequestContext(request))
	else:
		return render_to_response('admin/signin.html',locals(),context_instance=RequestContext(request))

def notice_del(request,id):
	if request.session.get('auth'):
		try:
			q = Notice.objects.get(nid=id)
			q.delete()
			return HttpResponse('1')
		except:
			return HttpResponse('0')
	else:
		return render_to_response('admin/signin.html',locals(),context_instance=RequestContext(request))

def edit(request,id):
	if request.session.get('auth'):
		q = {'nav2':'active'}
		try:
			q['q'] = Question.objects.get(qid=id)
		except:
			pass
		return render_to_response('admin/edit.html',locals(),context_instance=RequestContext(request))
	else:
		return render_to_response('admin/signin.html',locals(),context_instance=RequestContext(request))

def editq(request):
	if request.session.get('auth'):
		data = {'status':'0'}
		if 'qid' in request.POST:
			if request.POST['qid'] != '':
				try: 
					q = Question.objects.get(qid=request.POST['qid'])
					q.name=request.POST['name']
					q.source=request.POST['source']
					q.discribe=request.POST['discribe']
					q.date=time()
					q.point=request.POST['point']
					q.flag=request.POST['flag']
					q.tag=request.POST['tag']
					q.save()
					data['status'] = 1
					data['jump'] = reverse('admin.views.question')
				except:
					data['msg'] = "Wrong ID."
			else:
				try:
					Question.objects.create(name=request.POST['name'],
						source=request.POST['source'],
						discribe=request.POST['discribe'],
						date=time(),
						point=request.POST['point'],
						flag=request.POST['flag'],
						tag=request.POST['tag'])
					data['status'] = 1
					data['jump'] = reverse('admin.views.question')
				except:
					data['msg'] = "Post error."
		return HttpResponse(simplejson.dumps(data, ensure_ascii=False))
	else:
		return render_to_response('admin/signin.html',locals(),context_instance=RequestContext(request))

def delq(request,id):
	if request.session.get('auth'):
		try:
			q = Question.objects.get(qid=id)
			q.delete()
			return HttpResponse('1')
		except:
			return HttpResponse('0')
	else:
		return render_to_response('admin/signin.html',locals(),context_instance=RequestContext(request))

def delu(request,id):
	if request.session.get('auth'):
		try:
			u = User.objects.get(uid=id)
			u.delete()
			return HttpResponse('1')
		except:
			return HttpResponse('0')
	else:
		return render_to_response('admin/signin.html',locals(),context_instance=RequestContext(request))

def lock(request,id):
	if request.session.get('auth'):
		try:
			u = User.objects.get(uid=id)
			u.status = 0
			u.save()
			return HttpResponse('1')
		except:
			return HttpResponse('0')
	else:
		return render_to_response('admin/signin.html',locals(),context_instance=RequestContext(request))

def unlock(request,id):
	if request.session.get('auth'):
		try:
			u = User.objects.get(uid=id)
			u.status = 1
			u.save()
			return HttpResponse('1')
		except:
			return HttpResponse('0')
	else:
		return render_to_response('admin/signin.html',locals(),context_instance=RequestContext(request))