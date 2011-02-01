#!/usr/bin/env python
# Grep ALL access lists for a specified pattern
# Refactoring code

import os.path
import pwd
import re
import sys
from acctutils.models import User
from acctutils.custom_exceptions import ObjectNotFound

GROUP_GID = 2000
DRUPAL_CURRENT = '6.19' #add more

def usage():
    print os.path.basename(sys.argv[0]) + ": REGEX"

def search_outdated(user_dir):
    #if is_drupal(user_dir)
    print find_drupal(user_dir)
    print find_wordpress(user_dir)

def find_drupal(user_dir):
    cmd = 'find ' + user_dir + '/web -name CHANGELOG.txt -print'
    files = []
    for file in os.popen(cmd).readlines():
        files.append(file[:-1])
    for file in files:
        try:
            f = open(file, "r")
            f.readline()
            f.readline()
            line = f.readline()
            result = re.match("Drupal (\d*\.\d*), ", line)
            if result:
                return result.group(1)
        except IOError:
            return None 
    return None

def find_wordpress(user_dir):
    cmd = 'find ' + user_dir + '/web -name readme.html -print'
    files = []
    for file in os.popen(cmd).readlines():
        files.append(file[:-1])
    for file in files:
        try:
            f = open(file, "r")
            for line in f.readlines():
                result = re.match("Version (\d*\.\d*\.\d*)", line)
                if result:
                    return result.group(1)
        except IOError:
            return None 
    return None

def find_awesomeness(user_dir):
    cmd = 'find ' + user_dir + '/web -name modules  -type d -print'
    dirs = []
    for file in os.popen(cmd).readlines():
        dirs.append(file[:-1])
    for dir in dirs:
    #for root, dirs, files in os.walk(user_dir):
    #    for file in [f for f in files if f == filename]:
    #        return file

        try:
            f = open(dir + "/system/system.module", "r")
            pattern = re.compile("define\('VERSION', '(\d*\.\d*)'\);")
            for line in f:
                m = pattern.match(line)
                if m:
                    return m.group(1)
            return None
        except IOError:
            return None

if __name__ == "__main__":
    try:
        user_dir = sys.argv[1]
    except IndexError:
        usage()
        sys.exit(0)

    try:
        search_outdated(user_dir)
    except KeyboardInterrupt:
        print '^C'
