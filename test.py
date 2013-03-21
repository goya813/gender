# coding: utf-8

phrase_file = open("../phrasePolDic.csv", "r");
phrase_dic = {};
for line in phrase_file:
	key = line.split(',')[0];
	value = line.split(',')[1];
	phrase_dic[key] = value;

phrase_file.close();

print phrase_dic["優柔不断"];
