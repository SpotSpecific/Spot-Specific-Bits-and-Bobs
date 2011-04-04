#!/usr/bin/env python
# encoding: utf-8
"""
Docudroid (docudroid.py)

This script generates MediaWiki-compatible markup for JavaScript classes in conjuntion with jsdoc-toolkit and a set of suitable templates, then uploads the resulting files to a pre-defined namespace in a specified MediaWiki installation of choice.

The jsdoc-toolkit scripts and templates do all the heavily lifting. This script manages their invokation, and the editing of the wiki pages to reflect new content.

Usage:
	After setting configuration variables in the 'Configuration' section below, invoke the script from the shell without arguments, e.g.
		./docudroid.py
		or
		python docudroid.py


Created by Graeme West on 2011-02-01.
Copyright (c) 2011 Spot Specific Ltd.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of the Spot Specific Ltd. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

# BEGIN Configuration

# The namespace (i.e. prefix) into which pages should be added in MediaWiki
wiki_namespace = "API Reference: "

# The directory where source JavaScript files to document reside. Include the trailing slash.
js_dir = '/path/to/the/js/to/be/documented/'

# The directory where generated HTML documentation files should reside. Include the trailing slash.
html_dir = '/path/to/where/the/resulting/html/files/should/go/'

# The relative path of the directory where generated HTML documentation files for symbols will reside. This is appended to html_dir. Don't change this unless jsdoc-toolkit's scripts require it.
symbols_dir = html_dir + 'symbols'

# The command to run to actually generate the HTML docs. In our local installation, we have absolute paths in this command. Basically, the js_dir gets appended to this generic command in order to specify which JS files the script should act upon.
# Change all paths as required.
jsdocs_gen_command = 'java -jar /path/to/jsdoc-toolkit/jsrun.jar /path/to/jsdoc-toolkit/app/run.js -a --directory=' + html_dir +'  -s -t=/path/to/jsdoc-toolkit/templates/mediawiki/ ' + js_dir

# MediaWiki username and password
wiki_username='username'
wiki_password='password'

# MediaWiki API endpoint
wiki_site = "http://my.company.com/wiki/api.php"

# the name of the index template (which gets dynamically baked into every class listing by Mediawiki)
index_template_name = "Template:Classlist"

# END Configuration


import sys
import os, glob

from wikitools import wiki
from wikitools import api
from wikitools import page

import collections

import subprocess

# Gets a specially-formatted symbol identifier from a JSdoc Toolkit output file which 
# has been generated using the MediaWiki templates. This is of the form:
# <!--SYMBOL=The Symbol Name Goes Here
# This script uses the content of that comment to determine which page name it should
# upload the wiki-formatted JSdoc to.

def extract_symbol_name_from_jsdoc(path=""):
	f = open(path)
	g = open(path)
	page_content = f.read()

	symbolname = ""
	for line in g.readlines():
		if line.startswith( "<!--SYMBOL=" ):
			symbolname = line.replace('<!--SYMBOL=', '', 1).strip()
	
	print "Extracted the following symbol name from JSdocs: '" + symbolname + "'"
	
	return symbolname, page_content
			

# Create or update content on a named MediaWiki page
def wiki_create_or_update(pagename="", content=""):
	print pagename
	try:
		test = page.Page(site, pagename)
		print "Got page: '" + pagename + "'"
		try:
			test.edit(text=content)
			print "Successfully updated page: '" + pagename + "'"
		except:
			print "Error: Could not edit page."
	except:
		print "Error: Could not get page from MediaWiki."

# Get the contents of index.html to use in the class index template
def get_index():
	index_path = os.path.join(html_dir, 'index.html')
	f = open(index_path)
	
	index_content = f.read()
	
	return index_content


if __name__ == '__main__':

	# Generate the actual JSDoc documentation by invoking jsdoc's jar file.
	# Better error handling here would be a Good Thing™. 
	try:
		subprocess.call([jsdocs_gen_command, '-1'], shell=True)
		print "Successfully regenerated JSDoc documentation."
	except:
		print "Error: could not regenerate JSDoc documentation."
	# Connect and log in to MediaWiki
	try:
		site = wiki.Wiki(wiki_site)
		print "Successfully connected to wiki."
		try:
			site.login(username=wiki_username, password=wiki_password)
			print "Successfully logged in to wiki."
		except:
			print "Error: Could not log in to wiki."
	except:
		print "Error: Could not connect to wiki."

	# Iterate through the list of class jsdoc files in the symbols directory 
	# which jsdoc-toolkit created, then extract the relevant pieces of info
	# from them.
	for infile in glob.glob(os.path.join(symbols_dir, '*.html')):
		print "current symbol file is: " + infile
		
		this_symbol_name, this_page_content = extract_symbol_name_from_jsdoc(infile)
		complete_page_name = wiki_namespace + this_symbol_name

		wiki_create_or_update(pagename=complete_page_name, content=this_page_content)
	
	# finally, update the index template.
	wiki_create_or_update(pagename=index_template_name, content=get_index())
	print "Successfully updated the index page template."