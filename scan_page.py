from BeautifulSoup import BeautifulSoup
import urllib2
import re
from sys import stdin
import urllib
import shutil
from urlparse import urlparse
from os.path import splitext, basename
import ntpath

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
		dl_ln = ln
		ln = urllib.unquote(ln)
		print str(i)+"================================================="
		print "link found:"
		print "Link: "+ln
		print "Title: "+title
		print "=================================================="
		disassembled = urlparse(ln)
		filename, file_ext = splitext(basename(disassembled.path))
		#Delete digits
		filename = ''.join(i for i in filename if not i.isdigit())
		#Delete underscores
		filename = filename.replace("_","")
		#Replace spaces by underscores
		filename = filename.replace(" ","_")

		doc = 'archive/'+filename+file_ext

		for ext in allowed_types:
			if doc.endswith(ext):
				if 'Y' in dl:
					dlreq = urllib2.Request(dl_ln, headers={'User-Agent' : "Magic Browser"}) 
					content = urllib2.urlopen(dlreq)
					output = open(doc,'w+')
					output.write(content.read())
					output.close()

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
	i=i+1	    

