#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script, that lets you post jekyll Blogposts with your browser and then lets jekyll create the page again.

todo:
	- maybe some safety stuff would be good

-----------------------------------------------------------------------------
"THE NERD-WARE LICENSE" (Revision 1):
<viirus@pherth.net> wrote this file. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me/us a beer, mate or some food in return
Phillip Thelen
-----------------------------------------------------------------------------
"""

# CGI
import sys
sys.stderr = sys.stdout
import cgi, cgitb, os, subprocess, re, urllib2, datetime, platform
cgitb.enable()

urlname = "jekyllpost.py"
jekyllpath = "/var/www/py.pherth.net/pages/"

class Index():

	def __init__(self):
		print "Content-type: text/html"
		print
		self.form = cgi.FieldStorage()
		if self.form.getvalue("save") != None:
			currdate = datetime.date.today()
			datestring = "{0}-{1}-{2}".format(currdate.year, currdate.month, currdate.day)
			entry = self.form.getvalue("entry")
			title = self.getTitle(entry)
			filename = datestring + "-" + title
			f = open((jekyllpath + "_posts/" + filename), "w")
			f.write(entry)
			f.close()
			os.system("cd" + jekyllpath + " && jekyll")
			print "<h1 style='color:red;'>Entry was posted successfully</h1>"

		self.printHead()
		self.printForm()
		self.printFooter()


	def printHead(self):
		print """
			<DOCTYPE! html>
			<head>
				<title>Create a new entry</title>
			</head>
			<body>"""
			

	def printForm(self):
		print """
		<h2>Create a new Post</h2>
			<form action="jekyllpost.py" method="post">
				<fieldset>
					<textarea name="entry" cols="50" rows="10">
---
layout: post
title: 
---
</textarea>
					<Button class="btn btn-primary" type="submit" name="save" value="1">Post</button>
					<button class="btn">Cancel</button>
				</fieldset>
			</form>"""

	def printFooter(self):
		print """
		</body>
		</html>"""


	def getTitle(self, entry):
		entry = entry.splitlines(True)
		for line in entry:
			if (line[0:6] == "title:"):
				title = line[6:]
				title = title.strip()
				title = title.replace(" ", "-")
				return title + ".markdown"

if __name__ == '__main__':
	Index()