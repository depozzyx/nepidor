import datetime
now = datetime.datetime.now()
def startup(dtext):
	m = open("content/log.txt", "a")
	if dtext=='Logging started at ':
		m.write('\n')
		m.write('\n')
		m.write('\n')
		m.write('[STARTUP] '+dtext+str(now)+'\n')
		print('[STARTUP] '+dtext+str(now))
	else:
		m.write('[STARTUP] '+dtext+'\n')
		print('[STARTUP] '+dtext)
	m.close()

startup('Logging started at ')

TOKEN = "1078592494:AAHEtx5glyyvNJkPmbEWa4nPEqAMX9QC-qQ"
startup('Token loaded')

USERS = []
users_loaded = 0
#560399754 - depozzyч
# # read users
# f = open("content/members.txt", "r")	
# spltd = f.read()
# spltd = spltd.split()
# USERS= list(spltd)
# f.close()
# startup('Users loaded, Array: '+str(USERS))



