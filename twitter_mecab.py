# coding: utf-8

import json;
import urllib;
import MeCab;
import re;
import twitter_gender;

url = "http://api.twitter.com/1/statuses/user_timeline.json";
tagger = MeCab.Tagger('-Ochasen');

f = open("twitter_mecab.csv", "w");
f.write("original,hinsi,trend\n");

pf = open("twitter_phrase.csv", "w");
pf.write("id,pol\n");

phrase_file = open("../phrasePolDic.csv", "r");
phrase_dic = {};
for line in phrase_file:
	key = line.split(',')[0];
	value = line.split(',')[1];

	phrase_dic[key] = value;

twitter_list = twitter_gender.get_genderlist();
count = {};
count["m"] = 0;
count["f"] = 0;
word_count = {};
word_count["m"] = {};
word_count["f"] = {};
word_count["trend"] = {};

def my_mecab(text):
	encoded_text = text.encode('utf-8');
	
	word_list = [];
	node = tagger.parseToNode(encoded_text);
	
	while (node):
		encoded_surface = node.surface;
		if (encoded_surface != ""):
			encoded_feature = node.feature;
			surface = encoded_surface.decode('utf-8');
			feature = encoded_feature.decode('utf-8');
			feature = feature.split(',')[0];

			word_list.append("%s,%s" % (surface, feature));

		node = node.next;

	return (word_list);

for tid, gender in twitter_list.items():
	print tid;
	param = {"screen_name" : tid, "count" : "200"};
	res = urllib.urlopen(url + "?" + urllib.urlencode(param));

	tweet_json_list = json.load(res);

	phrase_pol = 0;
	for tweet_json in tweet_json_list:
		tweet = tweet_json["text"];
		if (re.search("http", tweet)):
			continue;
		
		word_list = my_mecab(tweet);
		for word in word_list:
			count[gender] += 1;

			if (word_count[gender].has_key(word) == True):
				word_count[gender][word] += 1;
			else:
				word_count[gender][word] = 1;
			
			origin = word.split(",")[0].encode('utf-8');
			if (phrase_dic.has_key(origin) == True):
				phrase_pol += int(phrase_dic[origin].rstrip('\n'));

	pf.write("%s,%d\n" % (tid, phrase_pol));
			

for key, value in sorted(word_count["f"].items(), key=lambda x:x[1]):
	word_count["trend"][key] = float(value) / count["f"];

for key, value in sorted(word_count["m"].items(), key=lambda x:x[1]):
	if (word_count["trend"].has_key(key) == True):
		word_count["trend"][key] -= (float(value) / count["m"]);
	else:
		word_count["trend"][key] = (float(value) / count["m"]);

for key, value in sorted(word_count["trend"].items(), key=lambda x:x[1]):
	f.write(("%s,%f\n" % (key, value)).encode("utf-8"));

f.close();

