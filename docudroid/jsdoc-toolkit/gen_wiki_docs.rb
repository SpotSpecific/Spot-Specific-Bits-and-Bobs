#!/usr/bin/env ruby
#
# Sample script for searching page contents in a Wiki
#
require 'media_wiki'

mw = MediaWiki::Gateway.new('http://maker.spotspecific.com/help_wiki/api.php')
mw.login('support', 'c3ntr4l')
mw.create('RubyTestPage', 'test content', 'Comment: a bot created this page.')