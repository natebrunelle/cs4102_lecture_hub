def fresh_lecture():
	return {
		'title': 'None',
		'date': 'None',
		'reading': 'None',
		'keywords': 'None',
		'slides': 'None',
		'pm_video': 'None',
		'am_video': 'None',
		'weblinks': 'None'
	      }

def tup2link(tup):
	link = "new Weblink('"
	link += tup[1]
	link += "', '"
	link += tup[0]
	link += "')"
	return link

def sanitize_str(string):
	if type(string) == type(''):
		return string.replace("'", "\\'")
	else:
		return string

def sanitize_lecture(lecture):
	return {k: sanitize_str(v) for k, v in lecture.items()}

def createlecture(lecture):
	lecture = sanitize_lecture(lecture)
	lecturestr = 'new Lecture(\n' #intro
	lecturestr += "'"+lecture['title'] + "', \n" #title
	lecturestr += "'" + lecture['keywords'] + "', \n" #keywords
	lecturestr += "'" + lecture['date'] + "', \n" #pubdate
	lecturestr += "['https://uva.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=" + lecture['pm_video'] + "', \n" #pm video
	lecturestr += "'https://uva.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=" + lecture['am_video'] + "'], \n" #am video
	lecturestr += "'http://www.cs.virginia.edu/~njb2b/cs4102/hub/slides/" + lecture['slides'] + ".pdf', \n" #pdf
	lecturestr += "'http://www.cs.virginia.edu/~njb2b/cs4102/hub/slides/" + lecture['slides'] + ".pptx', \n" #pptx
	lecturestr += "'" + lecture['reading'] + "', \n" #readings
	if lecture['weblinks'] != 'None':
		lecturestr += "[\n "
		for tup in lecture['weblinks']:
			lecturestr += tup2link(tup)
			lecturestr += ", "
		lecturestr += "\n]\n"
	else:
		lecturestr += "'None'\n"
	lecturestr += "), \n"
	return lecturestr

	

hub = open("index_test.html", 'w')
hubhead = open("hubhead", 'r')
hubtail = open("hubtail", 'r')
lecture_list = open("lecture_list.txt", 'r')

for line in hubhead.readlines():
	hub.write(line)
currlecture = {}
weblinks = []

for line in lecture_list.readlines():
	if line.strip().lower() == 'current':
		break
	if len(line.strip())>0:
		if line.strip() == 'lecture:':
			if len(currlecture) > 0:
				hub.write(createlecture(currlecture))
			currlecture = fresh_lecture()
			weblinks = []
		else:
			stripped = line.strip()
			parsed = line.split(': ')
			if parsed[0].strip() == 'weblink':
				weblinks.append((parsed[1].strip(),''))
				currlecture['weblinks'] = weblinks
			elif parsed[0].strip() == 'url':
				weblinks[-1] = (weblinks[-1][0], parsed[1].strip())
			elif len(parsed) == 2:
				currlecture[parsed[0].strip()] = parsed[1].strip()
hub.write(createlecture(currlecture))

for line in hubtail.readlines():
	hub.write(line)


