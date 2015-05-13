from BeautifulSoup import BeautifulSoup
import urllib2
import re
from sys import stdin
import urllib
import shutil
from urlparse import urlparse
from os.path import splitext, basename
import ntpath
import codecs

def main():
	allowed_types=['pdf','doc','docx','ppt','pptx']

	wg = raw_input('Please enter the working group id ')

	print 'Please enter the url to scan for files'
	url = stdin.readline()

	print 'Download all files? (Y/N)'
	dl = stdin.readline()

	target = open('file_seed.txt', 'a')

	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
	html_page = urllib2.urlopen(req)
	soup = BeautifulSoup(html_page)
	i=0
	for link in soup.findAll('a'):
		ln = link.get('href')
		title = link.text
		alt = title.replace(" ","_")
	
		if not(ln is None):
			try:
				ln = urllib.unquote(ln)

				disassembled = urlparse(ln)
				filename, file_ext = splitext(basename(disassembled.path))
				#Delete digits
				filename = ''.join(i for i in filename if not i.isdigit())
				#Delete underscores
				filename = filename.replace("_","")
				#Replace spaces by underscores
				filename = filename.replace(" ","_")
				#Replace quotes
				filename = filename.replace("'","")
				filename = filename.replace(u'\u2019',"")

				#Replace quotes in title
				title = title.replace("'","")
				title = title.replace(u'\u2019',"")

				helper = urlparse(ln)
				dl_ln =  helper.scheme+'://'+helper.netloc+urllib.quote(helper.path)

				print str(i)+"================================================="
				print "link found:"
				print "Link: "+ln
				print "Link encoded: "+dl_ln
				print "Title: "+title
				print "=================================================="
			


				doc = 'archive/'+filename+file_ext
				skip = False

				for ext in allowed_types:
					if doc.endswith(ext):
						if 'Y' in dl:
							try:
								dlreq = urllib2.Request(dl_ln, headers={'User-Agent' : "Magic Browser"}) 
								content = urllib2.urlopen(dlreq)
								output = open(doc,'w+')
								output.write(content.read())
								output.close()
							except urllib2.HTTPError, e:
								print 'Error: Link is dead, skipping ...'
								skip = True
							except ValueError:
								special_link(doc,url,dl_ln)
								
							
						if skip is False:
							target.write('$jelle=\App\User::find(1);\n')
							target.write('$l'+str(i)+'= \App\Document::create(\n')
							target.write('[\n')
							target.write("'title' => '"+title+"',\n")
							target.write("'description' => '"+title+"',\n")
							target.write("'creator' => $jelle->id,\n")
							target.write(']\n')
							target.write(');\n')

							target.write('$f'+str(i)+'=\App\Resource::create(\n')
							target.write('[\n')
							target.write("'url'=>'/"+doc+"',\n")
							target.write("'filename' => '"+title+"',\n")
							target.write("'alt' => '"+alt+"',\n")
							target.write("'description' => '"+title+"',\n")
							target.write("'type'=> \App\Repositories\FileRepository::getType('"+doc+"')\n")
							target.write("]\n")
							target.write(");\n")
							target.write("$l"+str(i)+"->addFile($f"+str(i)+");\n")
							target.write("$l"+str(i)+"->setUser($jelle);\n")
							target.write("$l"+str(i)+"->setWorkgroup(\App\Workgroup::find("+str(wg)+"));\n")
							target.write("$l"+str(i)+"->save();\n\n\n")
							break
			except Exception as e:
				print ':-( Something went wrong, skipping link '+str(i)+' ...'
				print str(e)
		i=i+1
		skip = False	

def special_link(doc,url,ln):
	try:
		ln = urlparse(url).scheme+'://'+urlparse(url).netloc+urllib.quote(ln)
		print 'Unusual link: trying to download '+ln
		dlreq = urllib2.Request(ln, headers={'User-Agent' : "Magic Browser"}) 
		content = urllib2.urlopen(dlreq)
		output = open(doc,'w+')
		output.write(content.read())
		output.close()
	except urllib2.HTTPError, e:
		print 'Error: Link is dead, skipping ...'
		skip = True

main()
							
