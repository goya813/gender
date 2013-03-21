# coding: utf-8
# -*- coding: utf-8 -*-

import urllib;
import twitter_gender;
import json;
import MeCab;
import re;

append_flag = 1;

twitter_id = "pinkroot";
url = "http://api.twitter.com/1/statuses/user_timeline.json";
tagger = MeCab.Tagger('-Owakati');
count = {};
count["m"] = 0;
count["f"] = 0;
word_count = {};
word_count["m"] = {};
word_count["f"] = {};
word_count["trend"] = {};
twitter_list = twitter_gender.get_genderlist();

fp = open("gender_Analysis_female.csv", "w");
mp = open("gender_Analysis_male.csv", "w");
trendp = open("gender_Analysis_trend.csv", "w");

def my_mecab(text):
	encoded_text = text.encode('utf-8');
	encoded_result = tagger.parse(encoded_text);
	result = encoded_result.decode('utf-8');
	
	word_list = result.split(' ');
	return (word_list);

for tid, gender in twitter_list.items():
	print tid;
	param = {"screen_name" : tid, "count" : "200"};
	res = urllib.urlopen(url + "?" + urllib.urlencode(param));
	
	tweets_json = json.load(res);
	tweets_text = [];
	
	for tweet_json in tweets_json:
		tweet = tweet_json["text"];
		if (re.search("http", tweet) != None):
			continue;
		word_list = my_mecab(tweet);

		for word in word_list:
			if (word.isdigit() == True):
				continue;

			count[gender] += 1;
			if (word_count[gender].has_key(word) == True):
				word_count[gender][word] += 1;
			else:
				word_count[gender][word] = 1;
	
for key, value in sorted(word_count["f"].items(), key=lambda x:x[1]):
	#print "%s:%d" % (key, value);
	if (value > 10 and key != "\n"):
		word_count["trend"][key] = float(value) / count["f"];
		fp.write(("%s,%f\n" % (key, float(value) / count["f"])).encode("utf-8"));

for key, value in sorted(word_count["m"].items(), key=lambda x:x[1]):
	if (value > 10 and key != "\n"):
		mp.write(("%s,%f\n" % (key, float(value) / count["m"])).encode("utf-8"));
		if (word_count["trend"].has_key(key) == True):
			word_count["trend"][key] -= (float(value) / count["m"]);
		else:
			word_count["trend"][key] = float(value) / count["m"];
		
fp.write("%d" % count["f"]);
mp.write("%d" % count["m"]);

for key, value in sorted(word_count["trend"].items(), key=lambda x:x[1]):
	trendp.write(("%s,%f\n" % (key, value)).encode("utf-8"));

fp.close();
mp.close();
trendp.close();
