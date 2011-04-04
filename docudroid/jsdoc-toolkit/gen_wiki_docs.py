#!/usr/bin/env python
# encoding: utf-8
"""
gen_wiki_docs.py

Created by Graeme West on 2011-02-01.
Copyright (c) 2011 Spot Specific Ltd. All rights reserved.
"""

# Configuration
wiki_namespace = "API Reference: "
js_dir = '/u/DesignIsCentral/Spot-Runtime-UNCOMPRESSED/IPHONE_SPECIFIC/'
html_dir = '/u/DesignIsCentral/Documentation/SpotSpecific/API/Autogenerated/'
symbols_dir = html_dir + 'symbols/'

print symbols_dir

test_doc_path='/Users/graeme/git/jsdoc-toolkit/out/jsdoc/symbols/SC.View.html'


import sys
import os, glob

from wikitools import wiki
from wikitools import api
from wikitools import page

# Placeholder: this will be where jsdoc-toolkit is invoked to update the .html files 
# from the original JS files
def run_jsdoc():
	pass


# Gets a specially-formatted symbol identifier from a JSdoc Toolkit output file which 
# has been generated using the MediaWiki templates. This is of the form:
# <!--SYMBOL=The Symbol Name Goes Here
# This script uses the content of that comment to determine which page name it should
# upload the wiki-formatted JSdoc to.

def extract_symbol_name_from_jsdoc():
	f = open(test_doc_path)
	symbolname = ""
	for line in f.readlines():
		if line.startswith( "<!--SYMBOL=" ):
			symbolname = line.replace('<!--SYMBOL=', '', 1).strip()
	
	print "Extracted the following symbol name from JSdocs: '" + symbolname + "'"
	return symbolname
			

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

if __name__ == '__main__':

	# Connect and log in to MediaWiki
	try:
		site = wiki.Wiki("http://maker.spotspecific.com/help_wiki/api.php")
		print "Successfully connected to wiki."
		try:
			site.login(username="support", password="c3ntr4l")
			print "Successfully logged in to wiki."
		except:
			print "Error: Could not log in to wiki."
	except:
		print "Error: Could not connect to wiki."
	
	# this isn't ready yet, but will become the iteration code
	# for infile in glob.glob( os.path.join(symbols_dir, '*.html') ):
	# 	print "current symbol file is: " + infile
	
	complete_page_name = wiki_namespace + extract_symbol_name_from_jsdoc()

	wiki_create_or_update(pagename=complete_page_name, content="bob")