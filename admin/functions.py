# this file is for some extra function 

def checkAllow(filename):  
	allowExt = [".rar",".zip"]
	for i in range(0,len(allowExt)):
		if(filename.lower().endswith(allowExt[i])):
			return allowExt[i]
			return None

def writefile(path,upfile):
	fout = open(path,'wb')
	for chunk in upfile.chunks():
		fout.write(chunk)
	fout.close()	

