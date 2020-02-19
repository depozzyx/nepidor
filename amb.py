def debug(dtxt):
	print('[DEBUG] '+dtxt)

	d = open("content/log.txt", "a")
	d.write('[DEBUG] '+dtxt+'\n')
	d.close()

def log(dtxt):
	print('[LOG] '+dtxt)

	l = open("content/log.txt", "a")
	l.write('[LOG] '+dtxt+'\n')
	l.close()
