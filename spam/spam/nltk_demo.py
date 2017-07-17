#encoding=utf-8
# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import jieba
import nltk
#import sys
from nltk.classify.naivebayes import NaiveBayesClassifier

#s = [({'a': True , 'b' : False} , 1), ({'c' : True} ,1), ({'d':True} , 0)]
#r = ({'a':True, 'c':True })
#cf = NaiveBayesClassifier.train(s)
#print cf.classify(r)

def load_lines(file_name):
  f = open(file_name, 'r')
  lines = f.readlines()
  f.close()
  return lines

def load_stdin():
  lines = []
  for line in sys.stdin:
    lines.append(line)
  return lines

def stop_words_filter(words, stop_words):
  return words

def train():
  # train words
  words = load_stdin()
  fwords = stop_words_filter(words, stop_words)
  

words = []

lines = load_stdin()
for line in lines:
  word_list = jieba.cut(line)  
  for word in word_list:
    words.append(word)

#  print ','.join(word_list)

fl = nltk.FreqDist(word for word in words)

#print fl
for f,l in fl.items():
  print f , l

if __name__ == "__main__":
  stop_words_filename = ""
  stop_words = load_lines(stop_words_filename)
  # train
  # caculate


#def load_lines(file_name):
#  f = open(file_name,'r')
#  lines = f.readlines()
#  f.close()
#  return lines


#prob_classify

#str = '''微软公司提出以446亿美元的价格收购雅虎
#  中国网2月1日报道 美联社消息，微软公司提出以446亿美元现金加股票的价格收购搜索网站雅虎公司。
#  微软提出以每股31美元的价格收购雅虎。微软的收购报价较雅虎1月31日的收盘价19.18美元溢价62%。微软公司称雅虎公司的股东可以选择以现金或股票进行交易。
#  微软和雅虎公司在2006年底和2007年初已在寻求双方合作。而近两年，雅虎一直处于困境：市场份额下滑、运营业绩不佳、股价大幅下跌。对于力图在互联网市场有所作为的微软来说，收购雅虎无疑是一条捷径，因为双方具有非常强的互补性。(小桥)'''
  
#seg_list = jieba.cut(str, cut_all=True)

#print ', '.join(seg_list)
#print seg_list

#def stop_words(word):
#  words = [];
#  for word in seg_list:
#  word = word.strip()
#  if len(word) > 0:
#    words.append(word)
#
#fl = nltk.FreqDist(word for word in words)
#
#for k,v in fl.iteritems():
#  print k, v



