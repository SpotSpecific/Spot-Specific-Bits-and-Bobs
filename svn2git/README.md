svn2git
=======
A simple dropin shellscript that nags you with wee reminders every time you try to use svn instead of git.

Pre-requisites
--------------
svn  
git  
the ability to insert aliases into your standard shell RC file (.bash_profile on MacOS)

Install
-------
    mv svn2git /usr/local/bin/
    chmod a+x /usr/local/bin/svn2git

modify your shell RC file and create two aliases
1. alias realsvn="/usr/bin/svn"
2. alias svn="/usr/local/bin/svn2git"

MORE INFO
- [https://github.com/SpotSpecific/Spot-Specific-Bits-and-Bobs/tree/master/svn2git] (https://github.com/SpotSpecific/Spot-Specific-Bits-and-Bobs/tree/master/svn2git)
