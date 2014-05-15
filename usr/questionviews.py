from django.core.paginator import Paginator
from usr.models import Question,User

_questionMap = {
	'misc':'nav2',
	'crypto':'nav3',
	'forensics':'nav4',
	'pwnables':'nav5',
	'reverse':'nav6',
	'web':'nav7',
}

_qTypeMap = {
	'misc':'M',
	'crypto':'C',
	'forensics':'F',
	'pwnables':'P',
	'reverse':'R',
	'web':'W',
}

def init_q():
	q = {'error':''}
	return q

def question_view(type,uid,page):
	q = init_q()
	try:
		q[_questionMap.get(type)] = 'active'
		try:
			paginator =  Paginator(Question.objects.order_by('-qid').filter(tag=_qTypeMap.get(type)),12)
			q['list'] = paginator.page(page)
			q['pagenow'] = page
			q['pageall'] = paginator.num_pages
			q['pagepre'] = int(page) - 1
			q['pagenex'] = int(page) + 1
			for r in q['list']:
				if r.is_passed(uid):
					setattr(r,'pass',1)
				else:
					setattr(r,'pass',0)
		except Exception,e:
			q['error'] = 'database error [questionView] %s %s' % (Exception,e)
	except Exception,e:
		q['error'] = 'error type[%s]' % type
	return q

def question_detial(qid,uid):
	q = init_q()
	try:
		q['q'] = Question.objects.get(qid=qid)
		if q['q'].is_passed(uid):
			q['pass'] = 1
		else:
			q['pass'] = 0
	except Exception,e:
		q['error'] = 'database error [questionDetial]'
	return q

def solve_question(qid,uid,flag):
	r = {'status':0}
	try:
		q = Question.objects.get(qid=qid).resolve(uid,flag)
		r['status'] = q  
		if q == 0:
			r['msg'] = 'database error [solveQuestion]'
	except:
		r['msg'] = 'wrong question!'
	return r
