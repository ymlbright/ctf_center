from django.db import models
import hashlib
from time import time,localtime,strftime
# Create your models here.
class Question(models.Model):
	TAG=(
		(u'M',u'misc'),
		(u'C',u'crypto'),
		(u'F',u'forensics'),
		(u'P',u'pwnables'),
		(u'R',u'reverse'),
		(u'W',u'web')
	)
	qid = models.AutoField(primary_key=True, db_index=True)
	name = models.CharField(max_length=20)
	source = models.CharField(max_length=20)
	discribe = models.CharField(max_length=600)
	date = models.IntegerField(default=0)
	point = models.IntegerField(default=0)
	flag = models.CharField(max_length=200)
	tag = models.CharField(max_length=2,choices=TAG)
	passed = models.IntegerField(default=0)
	submitted = models.IntegerField(default=0)

	def is_passed(self,uid):
		if uid == '':
			return False
		try:
			p = ScoreLog.objects.get(uid=uid,qid=self.qid)
			return True
		except:
			return False

	def get_date(self):
		x = localtime(self.date)
		return strftime('%Y-%m-%d %H:%M:%S',x)

	def resolve(self,uid,flag):
		if flag==self.flag:
			try:
				n = ScoreLog.objects.get(uid=uid,qid=self.qid)
				return 1
			except:
				self.submitted = self.submitted + 1
				try:
					u = User.objects.get(uid=uid);
					u.score = u.score + self.point
					u.save()
					n = ScoreLog.objects.create(uid=u,qid=self,date=time())
					self.passed = self.passed + 1
					self.save()
					return 1
				except:
					self.save()
					return 0
		else:
			self.save()
			return -1

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name

class User(models.Model):
	uid = models.AutoField(primary_key=True, db_index=True)
	name = models.CharField(max_length=20)
	pwd = models.CharField(max_length=40)
	email = models.CharField(max_length=50)
	lastlogin = models.IntegerField(default=0)
	loginip = models.CharField(max_length=40)
	score = models.IntegerField(default=0)
	status = models.CharField(max_length=16,default='0')

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name

	def login(self,pwd,ip):
		if hashlib.sha1(pwd).hexdigest() == self.pwd:
			if self.status == '1':
				self.loginip = ip
				self.lastlogin = time()
				self.save()
				return 1
			else:
				return -1
		else:
			return 0

	def passed(self):
		try:
			return ScoreLog.objects.filter(uid=self)
		except:
			return None

	def is_locked(self):
		if self.status != '1':
			return True
		else:
			return False


class ScoreLog(models.Model):
	sid = models.AutoField(primary_key=True)
	uid = models.ForeignKey(User,db_index=True)
	qid = models.ForeignKey(Question)
	date = models.IntegerField(default=0)

	def __str__(self):
		return self.uid

class Notice(models.Model):
	nid = models.AutoField(primary_key=True)
	date = models.IntegerField(default=0)
	content = models.CharField(max_length=600)

	def get_date(self):
		x = localtime(self.date)
		return strftime('%Y-%m-%d %H:%M:%S',x)

''''
class Writeup(models.Model):
	qid = models.ForeignKey(Question,primary_key=True,db_index=True)
	uid = models.ForeignKey(User)
	artical = models.CharField(max_length=1000)

	def __str__(self):
		return self.qid
'''