# coding: utf-8

import MeCab;

text = u"MeCabで遊んでみよう！";

tagger = MeCab.Tagger('-Owakati');

encoded_text = text.encode('utf-8');
encoded_result = tagger.parse(encoded_text);
result = encoded_result.decode('utf-8');

print result;
