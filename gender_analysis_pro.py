# coding: utf-8

import urllib;
import twitter_gender;
import json;
import MeCab;
import re;

url = "http://api.twitter.com/1/statuses/user_timeline.json";
tagger = MeCab.Tagger('-Owakati');
trend_list = {};
twitter_list = twitter_gender.get_genderlist();

def my_mecab(text):
	encoded_text = text.encode('utf-8');
	encoded_result = tagger.parse(encoded_text);
	result = encoded_result.decode('utf-8');

	word_list = result.split(' ');
	return (word_list);
	
for line in  open("gender_Analysis_trend.csv", "r"):
	item_list = line[:-1].split(",");
	if (line[0] == ","): 
		trend_list[","] = float(item_list[2]);
	else:
		word = item_list[0];
		trend = item_list[1];
		trend_list[word] = float(trend);

success = 0;
for tid, gender in twitter_list.items():
	param = {"screen_name" : tid, "count" : "200", "page" : "2"};
	res = urllib.urlopen(url + "?" + urllib.urlencode(param));

	tweets_json = json.load(res);
	user_trend = 0.0;
	
	for tweet_json in tweets_json:
		tweet = tweet_json["text"];
		if (re.search("http", tweet) != None):
			continue;

		word_list = my_mecab(tweet);

		for word in word_list:
			if (trend_list.has_key(word) == True):
				user_trend += trend_list[word];
	
	user_gender = "";
	if (user_trend >= 0.0):
		user_gender = "f";
	else:
		user_gender = "m";
	print "正解:%s\t結果:%s trend:%f %s" % (gender, user_gender, user_trend, tid);
	if (gender == user_gender):
		success += 1;

print "%d/%d" % (success, len(twitter_list));

