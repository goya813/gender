# coding: UTF-8

import urllib, urllib2, sys;
from BeautifulSoup import BeautifulSoup;
import time;

OPENER = urllib2.build_opener();
OPENER.addheaders = [("User-Agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)")];

BASE_URL = "http://kroko.jp/ffbattle";
MY_DATA = {"id" : "tomo813", "pass" : "goyatomo813"};

fp = open("log.html", "w");

def save_res(res):
	fp.write(res);

def hash_cat(dest, src):
	for key in src:
		dest[key] = src[key];
	
	return (dest);

def doPost(post_data):
	req = urllib2.Request(BASE_URL + "/monster.cgi", post_data);
	res = urllib2.urlopen(req);

	save_res(res.read());

	return (res);

def goDungeon(dungeon_data):
	data = hash_cat(dungeon_data, MY_DATA);
	post_data = urllib.urlencode(data);
	res = doPost(post_data);
	
	return (res);

if __name__ == "__main__":
	dungeon_data = {"mode" : "monster0", "chck" : "2"};
	
	while (True):
		print "go dungeon";
		res = goDungeon(dungeon_data);
		print "end";
		time.sleep(10.0);	

	fp.close();	
