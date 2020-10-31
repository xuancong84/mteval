#!/usr/bin/env python2
# coding=utf-8

import os,sys,gzip,operator,math,copy,argparse,re,select,unicodedata, time
from itertools import *
from collections import *

enum=enumerate

def ee(msg=''):
	print >>sys.stderr, msg
	sys.exit(0)

def UpdateLocals(d):    # Warning: must call using "exec UpdateLocals(dict)"
	sys._getframe(1).f_locals.update(d)
	return ''

def helpMsg(msgs, wait_time=0.3):
	a,b,c=select.select([sys.stdin],[],[],wait_time)
	if not a:
		print >>sys.stderr, (msgs if type(msgs)==str else '\n'.join(msgs))

def Copy(obj):
	return copy.deepcopy(obj)

def Open(fn, mode='r'):
	if fn=='-':
		return sys.stdin if mode.startswith('r') else sys.stdout
	return gzip.open(fn, mode) if fn.lower().endswith('.gz') else open(fn, mode)

def LoadWordMLF(fp):
	entries=[]
	for L in fp:
		L=L.strip().decode('utf8')
		if len(L)<=0:
			continue
		if L[0]=='#':
			continue
		if L[0]=='"':
			label=L
			entry=[]
			continue
		if L[0]=='.':
			entries.append((label,entry))
			continue
		entry.append(L)
	return entries

def findAll(arr,obj):
	return [i for i,j in enum(arr) if j==obj]

def Convert(obj,typ):
	if type(obj)!=list:
		return typ(obj)
	return [Convert(i,typ) for i in obj]

def Exp(obj):
	if type(obj)!=list:
		return math.exp(obj)
	return [Exp(i) for i in obj]

def Log(obj):
	if type(obj)!=list:
		return math.log(obj)
	return [Log(i) for i in obj]

def ListOfDouble2Map(lod):
	map={}
	for (a,b) in lod:
		map[a]=b
	return map

def load(fi,verbose=10000,separator=None):
	fp=Open(fi) if type(fi)==str else fi
	if verbose!=0:
		print >>sys.stderr,'Loading',fi,'...'
	data=[]
	n=0
	for L in fp:
		if verbose!=0:
			n+=1
			if n%verbose==0:
				sys.stderr.write(str(n)+'\r')
		its=L.strip().split(separator)
		data.append(its)
	if verbose!=0:
		sys.stderr.write('Done!           \n')
	return data

def loadUTF8(fi,verbose=10000,separator=None):
	fp=Open(fi) if type(fi)==str else fi
	if verbose!=0:
		print >>sys.stderr,'Loading',fi,'...'
	data=[]
	n=0
	for L in fp:
		if verbose!=0:
			n+=1
			if n%verbose==0:
				sys.stderr.write(str(n)+'\r')
		its=L.strip().decode('utf8').split(separator)
		data.append(its)
	if verbose!=0:
		sys.stderr.write('Done!           \n')
	return data

def loadA(fi,verbose=16):
	fp=Open(fi) if type(fi)==str else fi
	if verbose!=0:
		print >>sys.stderr,'Loading',fi,'...'
	data=[]
	n=0
	for L in fp:
		if verbose!=0:
			n+=1
			if n%verbose==0:
				sys.stderr.write(str(n)+'\r')
		data.append(L.strip())
	if verbose!=0:
		sys.stderr.write('Done!           \n')
	return data

def read_linegroup(fp):
	ret=[]
	while True:
		L=fp.readline()
		if len(L)==0:
			if ret==[]:
				return None
			else:
				return ret
		its=L.strip().split()
		if len(its)==0:
			break
		ret.append(its)
	return ret

def read_linegroups(fp):
	ret=[]
	if type(fp)==str:
		fp=Open(fp)
	while True:
		lg=read_linegroup(fp)
		if lg==None:
			break
		ret+=[lg]
	return ret

def read_linegroupA(fp):
	ret=[]
	while True:
		L=fp.readline()
		if len(L)==0:
			if ret==[]:
				return None
			else:
				return ret
		its=L[0:-1]
		if len(its)==0:
			break
		ret.append(its)
	return ret

def read_linegroupsA(fp):
	ret=[]
	if type(fp)==str:
		fp=Open(fp)
	while True:
		lg=read_linegroupA(fp)
		if lg==None:
			break
		ret+=[lg]
	return ret

def ensure_dir(f):
	if not os.path.exists(f):
		os.makedirs(f)

def SelectColumn(data,n):
	if data==None:
		return None
	ret=[]
	for its in data:
		if len(its)>n:
			ret.append(its[n])
		else:
			ret.append('')
	return ret

def SelectColumns(data,indices):
	if data==None:
		return None
	ret=[]
	for its in data:
		ret.append([its[i] for i in indices])
	return ret

def SelectColumnsByRange(data,range):
# input data is a 2-d array
	ret=[]
	for row in data:
		ret.append([])
		for arg in args:
			i=arg.find('-')
			if i==(len(arg)-1):		# e.g. 5-
				start_pos=int(arg[:i])-1
				ret[-1].extend(row[start_pos:])
			elif i==0:				# e.g. -1
				pos=int(arg)
				if row!=[]:
					ret[-1].append(row[pos])
			elif i!=-1:				# e.g. 3-5
				start_pos=int(arg[:i])-1
				to=int(arg[i+1:])
				if to>=0:
					end_pos=to
				else:
					end_pos=len(row)+to
				ret[-1].extend(row[start_pos:end_pos])
			else:					# e.g. 5
				pos=int(arg)-1
				ret[-1].extend(row[pos:pos+1])
	return ret

def DeleteEmptyRows(data):
	out=[]
	for its in data:
		if its!=[]:
			out.append(its)
	return out

def DeleteEmptyCells(data):
	out=[]
	for i in data:
		if i!='':
			out.append(i)
	return out

def inc(m,e,val=1):
	if e in m:
		m[e]+=val
		return True
	else:
		m[e]=val
		return False

def dot(a,b):
	return sum(map(operator.mul,a,b))

def norm_logP(b):
	if len(b)==0:
		return []
	a=b
	mean=float(sum(a))/len(a)
	a=[i-mean for i in a]
	S=math.log(sum([math.exp(i) for i in a]))
	a=[i-S for i in a]
	return a

def norm_P(b):
	if len(b)==0:
		return []
	a=b
	S=float(sum(a))
	return [i/S for i in a]

def norm_logP_to_P(b):
	if len(b)==0:
		return []
	a=b[:]
	mean=float(sum(a))/len(a)
	a=[math.exp(i-mean) for i in a]
	S=sum(a)
	return [i/S for i in a]

def Normalize(a):
	l=math.sqrt(dot(a,a))
	return [i/l for i in a]

def Print(data,output=sys.stdout,delimiter=' '):
	for i in data:
		print >>output, delimiter.join([str(j) for j in i])

def saveToPath(data,path):
	fp=Open(path,'w')
	Print(data,fp)
	fp.close()

def savemap(fn,m):
	fp=gzip.open(fn,'w')
	N=len(m)
	n=0
	sys.stderr.write('Writing to '+fn+' ...\n')
	if type(m)==type({}):
		its=m.iteritems()
	else:
		its=iter(m)
	for i in its:
		n+=1
		if n%16==0:
			sys.stderr.write(str(n)+'/'+str(N)+'\r')
		print >>fp,i[0],i[1]
	fp.close()
	sys.stderr.write('Done             \n')

def Abs(data):
	return [abs(i) for i in data]

def mean(data):
	return sum(data)/float(len(data)) if len(data)>0 else 0.0

def dot(a,b):
	return sum(map(operator.mul,a,b))

def Add(a,b):
	return map(operator.add, a,b)

def Sub(a,b):
	return map(operator.sub, a,b)

def mul(vec,a):
	return [i*a for i in vec]

def Mul(v1,v2):
	return map(operator.mul, v1, v2)

def div(vec,a):
	a=float(a)
	return [i/a for i in vec]

def std(vec):
	S_x2=dot(vec,vec)
	S_x=sum(vec)
	std=math.sqrt((S_x2-float(S_x)*S_x/len(vec))/(len(vec)-1))
	return std

def HorizontalAppend(a,b):
	ret=[]
	for i in range(0,max(len(a),len(b))):
		if i>len(a):
			ret.append(b[i])
		elif i>len(b):
			ret.append(a[i])
		else:
			ret.append(a[i]+b[i])
	return ret

def count_match(array,e):
	n=0
	for i in array:
		if i==e:
			n+=1
	return n

def count_occur(str,dict):
	n=0
	for c in str:
		if c in dict:
			n+=1
	return n

def PrintTable(io,table,sep=' '):
	keys=[]
	for i in table:
		keys+=table[i].keys()
	keys=set(keys)
	for i in keys:
		io.write(sep+str(i))
	io.write('\n')
	for i in table:
		io.write(str(i)+sep)
		for j in keys:
			if j not in table[i]:
				table[i][j]='N.A.'
			io.write(str(table[i][j])+sep)
		io.write('\n')

def StripFileExt(fn):
	its=fn.split('.')
	if len(its)<=1:
		return fn,''
	return '.'.join(its[0:-1]),its[-1]

def joinInnerArray(a):
	out=[]
	for i in a:
		out+=i
	return out

def readURL(url):
	sock=urllib.urlopen(url)
	txt=sock.read()
	sock.close()
	return txt

def swap(a,b):
	[a,b]=[b,a]

def non_dup_items(data):
	s=set()
	out=[]
	for i in data:
		if i in s:
			continue
		s.add(i)
		out.append(i)
	return out


def KL(a,b):
	sum=0
	for i in range(0,len(a)):
		if a[i]>0:
			sum+=math.log(a[i]/b[i])*a[i]
	return sum

def build_dict(io,method):
	# return method=0:raw-count,N(w); 1:P(w); 2:logP(w)
	m=Counter()
	n=0
	for L in io:
		its=L.strip().split()
		m.update(its)
		n+=len(its)
	print >>sys.stderr,'file loaded, vocab-size=',len(m)
	if method==1:
		for i in m:
			m[i]=m[i]/float(n)
	if method==2:
		for i in m:
			m[i]=math.log(float(m[i])/n)
	return m

def build_list(io):
	ret=[]
	for L in io:
		for w in L.strip().split():
			ret+=[w]
	return ret

def xml_get_docid(L):
	docid=''
	genre=''
	for w in L[1:-1].split():
		if w.lower().startswith('docid='):
			docid=w[6:]
			if docid[0]==docid[-1]=='"':
				docid=docid[1:-1]
		elif w.lower().startswith('genre='):
			genre=w[6:]
			if genre[0]==genre[-1]=='"':
				genre=genre[1:-1]
	return [docid,genre]

def xml_get_seg(L,bInfo=False):
	p=L.find('>')
	assert p>0
	info1=L[0:p+1]
	L=L[p+1:]
	p=L.rfind('<')
	assert p>=0
	info2=L[p:]
	L=L[0:p]
	if bInfo:
		return L,info1,info2
	return L

# input FST is an list of maps, each map element is a pair of input/output, src=0 specifies the next map
# dst>=0: FST node index; dst=-1: abort and reject; dst=string, accept and returns the string
# return -1: abort reject; -2: normal reject; 'string':last target
def FST_match(arr,i,fst,j):
	if i>=len(arr):
		return -2
	if arr[i] not in fst[j]:
		return -2
	e=fst[j][arr[i]]
	for n in fst[j][0]:
		if n==-1:
			return -1
		if type(n)==int and n>=0:
			n=FST_match(arr,i+1,fst,n)
			if n==-1:
				return -1
			if n==-2:
				continue
			return [e]+n
		return [e,n]
	return -2

def FST_transform(arr,fst,func):
	i=0
	while i<len(arr):
		hist=FST_match(arr,i,fst,0)
		if type(hist)==list:
			arr[i:i+len(hist)-1]=[func(hist)]
		i+=1

def get_word_pos(w):
	n=w.count('/')
	if n==1:
		return w.split('/')
	if n==0:
		return [w,'null']
	if w[-1]=='/':
		return [w[0:-2],'/']
	p=w.rfind('/')
	return [w[0:p],w[p+1:]]

def trim(s):
	return ' '.join(s.split())

_fw2hw_ascii={'，':',', '。':'.', '？':'?', '！':'!', '、':',', '：':':', '；':';', '＇':"'", '＂':'"', '“':'"', '”':'"', '‘':"'", '’':"'",
   '１':'1', '２':'2', '３':'3','４':'4','５':'5','６':'6','７':'7','８':'8','９':'9','０':'0',
   'ａ':'a','ｂ':'b','ｃ':'c','ｄ':'d','ｅ':'e','ｆ':'f','ｇ':'g','ｈ':'h','ｉ':'i','ｊ':'j','ｋ':'k','ｌ':'l','ｍ':'m','ｎ':'n','ｏ':'o','ｐ':'p','ｑ':'q','ｒ':'r','ｓ':'s','ｔ':'t','ｕ':'u','ｖ':'v','ｗ':'w','ｘ':'x','ｙ':'y','ｚ':'z',
   'Ａ':'A','Ｂ':'B','Ｃ':'C','Ｄ':'D','Ｅ':'E','Ｆ':'F','Ｇ':'G','Ｈ':'H','Ｉ':'I','Ｊ':'J','Ｋ':'K','Ｌ':'L','Ｍ':'M','Ｎ':'N','Ｏ':'O','Ｐ':'P','Ｑ':'Q','Ｒ':'R','Ｓ':'S','Ｔ':'T','Ｕ':'U','Ｖ':'V','Ｗ':'W','Ｘ':'X','Ｙ':'Y','Ｚ':'Z',
   '．':'.','…':'...','％':'%','＠':'@','＄':'$','＃':'#','－':'-','—':'-','─':'-','～':'~','〜':'~','／':'/','（':'(','）':')','【':'[','】':']','［':'[','］':']','｛':'{','｝':'}','『':'"','「':'"','』':'"',
   '」':'"','《':'"','》':'"','〔':'"','〕':'"','＿':'_','￣':'-','━':'-','＊':'*','﹚':')','﹙':'(','・':'·','﹒':'.','﹖':'?',' ':' ','　':' ','｜':'|', '•':'·'
}
_fw2hw_utf8={k.decode('utf8'):v.decode('utf8') for k,v in _fw2hw_ascii.iteritems()}
def fw2hw(L):
	if type(L)==str:
		return ''.join([(_fw2hw_utf8[c] if c in _fw2hw_utf8 else c) for c in L.decode('utf8', 'ignore')]).encode('utf8')
	else:
		return ''.join([(_fw2hw_utf8[c] if c in _fw2hw_utf8 else c) for c in L])

def fw2hw_builtin(L, mode='NFKC'):
	return unicodedata.normalize(mode, L.decode('utf8', 'ignore')).encode('utf8')

def isChineseCharacter(uc):
	return ord(uc)>=0x4e00 and ord(uc)<=0x9fff


_digraphs={u'ﬀ':'ff', u'ﬃ':'ffi', u'ﬄ':'ffl', u'ﬁ':'fi', u'ﬂ':'fl', u'Ǳ':'DZ', u'ǲ':'Dz', u'ǳ':'dz',
           u'Ĳ':'IJ', u'ĳ':'ij', u'Ǉ':'LJ', u'ǈ':'Lj', u'ǉ':'lj', u'Ǌ':'NJ', u'ǋ':'Nj', u'ǌ':'nj'}
def convertDigraphLigature(L):
	sin = L.decode('utf8', 'ignore') if type(L)==str else L
	sout = ''.join([(_digraphs[c] if c in _digraphs else c) for c in sin])
	return sout.encode('utf8') if type(L)==str else sout


class BPE(object):
	def __init__(self, codes, separator='@@', vocab=None, glossaries=None):

		# check version information
		firstline = codes.readline()
		if firstline.startswith('#version:'):
			self.version = tuple([int(x) for x in re.sub(r'(\.0+)*$', '', firstline.split()[-1]).split(".")])
		else:
			self.version = (0, 1)
			codes.seek(0)

		self.bpe_codes = [tuple(item.split()) for item in codes]

		# some hacking to deal with duplicates (only consider first instance)
		self.bpe_codes = dict([(code, i) for (i, code) in reversed(list(enumerate(self.bpe_codes)))])
		self.bpe_codes_reverse = dict([(pair[0] + pair[1], pair) for pair, i in self.bpe_codes.items()])
		self.separator = separator
		self.vocab = vocab
		self.glossaries = glossaries if glossaries else []

	def segment(self, sentence):
		"""segment single sentence (whitespace-tokenized string) with BPE encoding"""
		if type(sentence)==str:
			return self.segment(sentence.decode('utf8', 'ignore')).encode('utf8')

		output = []
		for word in sentence.split():
			new_word = [out for segment in self._isolate_glossaries(word)
			            for out in BPE.encode(segment,
			                              self.bpe_codes,
			                              self.bpe_codes_reverse,
			                              self.vocab,
			                              self.separator,
			                              self.version,
			                              self.glossaries)]

			for item in new_word[:-1]:
				output.append(item + self.separator)
			output.append(new_word[-1])

		return ' '.join(output)

	def segment_word(self, word):
		"""segment single sentence (whitespace-tokenized string) with BPE encoding"""
		if type(word)==str:
			out = self.segment_word(word.decode('utf8', 'ignore'))
			return [w.encode('utf8') for w in out]

		output = []
		new_word = [out for segment in self._isolate_glossaries(word)
		            for out in BPE.encode(segment,
		                              self.bpe_codes,
		                              self.bpe_codes_reverse,
		                              self.vocab,
		                              self.separator,
		                              self.version,
		                              self.glossaries)]

		return [w+self.separator for w in new_word[:-1]]+[new_word[-1]]

	def _isolate_glossaries(self, word):
		word_segments = [word]
		for gloss in self.glossaries:
			word_segments = [out_segments for segment in word_segments
			                 for out_segments in BPE.isolate_glossary(segment, gloss)]
		return word_segments

	@staticmethod
	def get_pairs(word):
		"""Return set of symbol pairs in a word.
		word is represented as tuple of symbols (symbols being variable-length strings)
		"""
		pairs = set()
		prev_char = word[0]
		for char in word[1:]:
			pairs.add((prev_char, char))
			prev_char = char
		return pairs

	@staticmethod
	def encode(orig, bpe_codes, bpe_codes_reverse, vocab, separator, version, glossaries=None, cache={}):
		"""Encode word based on list of BPE merge operations, which are applied consecutively"""

		if orig in cache:
			return cache[orig]

		if orig in glossaries:
			cache[orig] = (orig,)
			return (orig,)

		if version == (0, 1):
			word = tuple(orig) + ('</w>',)
		elif version == (0, 2):  # more consistent handling of word-final segments
			word = tuple(orig[:-1]) + (orig[-1] + '</w>',)
		else:
			raise NotImplementedError

		pairs = BPE.get_pairs(word)

		if not pairs:
			return orig

		while True:
			bigram = min(pairs, key=lambda pair: bpe_codes.get(pair, float('inf')))
			if bigram not in bpe_codes:
				break
			first, second = bigram
			new_word = []
			i = 0
			while i < len(word):
				try:
					j = word.index(first, i)
					new_word.extend(word[i:j])
					i = j
				except:
					new_word.extend(word[i:])
					break

				if word[i] == first and i < len(word) - 1 and word[i + 1] == second:
					new_word.append(first + second)
					i += 2
				else:
					new_word.append(word[i])
					i += 1
			new_word = tuple(new_word)
			word = new_word
			if len(word) == 1:
				break
			else:
				pairs = BPE.get_pairs(word)

		# don't print end-of-word symbols
		if word[-1] == '</w>':
			word = word[:-1]
		elif word[-1].endswith('</w>'):
			word = word[:-1] + (word[-1].replace('</w>', ''),)

		if vocab:
			word = BPE.check_vocab_and_split(word, bpe_codes_reverse, vocab, separator)

		cache[orig] = word
		return word

	@staticmethod
	def recursive_split(segment, bpe_codes, vocab, separator, final=False):
		"""Recursively split segment into smaller units (by reversing BPE merges)
		until all units are either in-vocabulary, or cannot be split futher."""

		try:
			if final:
				left, right = bpe_codes[segment + '</w>']
				right = right[:-4]
			else:
				left, right = bpe_codes[segment]
		except:
			# sys.stderr.write('cannot split {0} further.\n'.format(segment))
			yield segment
			return

		if left + separator in vocab:
			yield left
		else:
			for item in BPE.recursive_split(left, bpe_codes, vocab, separator, False):
				yield item

		if (final and right in vocab) or (not final and right + separator in vocab):
			yield right
		else:
			for item in BPE.recursive_split(right, bpe_codes, vocab, separator, final):
				yield item

	@staticmethod
	def check_vocab_and_split(orig, bpe_codes, vocab, separator):
		"""Check for each segment in word if it is in-vocabulary,
		and segment OOV segments into smaller units by reversing the BPE merge operations"""

		out = []

		for segment in orig[:-1]:
			if segment + separator in vocab:
				out.append(segment)
			else:
				# sys.stderr.write('OOV: {0}\n'.format(segment))
				for item in BPE.recursive_split(segment, bpe_codes, vocab, separator, False):
					out.append(item)

		segment = orig[-1]
		if segment in vocab:
			out.append(segment)
		else:
			# sys.stderr.write('OOV: {0}\n'.format(segment))
			for item in BPE.recursive_split(segment, bpe_codes, vocab, separator, True):
				out.append(item)

		return out

	@staticmethod
	def read_vocabulary(vocab_file, threshold):
		"""read vocabulary file produced by get_vocab.py, and filter according to frequency threshold."""

		vocabulary = set()

		for line in vocab_file:
			word, freq = line.split()
			freq = int(freq)
			if threshold == None or freq >= threshold:
				vocabulary.add(word)

		return vocabulary

	@staticmethod
	def isolate_glossary(word, glossary):
		"""
		Isolate a glossary present inside a word.
		Returns a list of subwords. In which all 'glossary' glossaries are isolated
		For example, if 'USA' is the glossary and '1934USABUSA' the word, the return value is: ['1934', 'USA', 'B', 'USA']
		"""
		if word == glossary or glossary not in word:
			return [word]
		else:
			splits = word.split(glossary)
			segments = [segment.strip() for split in splits[:-1] for segment in [split, glossary] if segment != '']
			return segments + [splits[-1].strip()] if splits[-1] != '' else segments


g_file_timestamp = {}
def check_file_timestamp(filename):
	# it returns:
	# 0: no change; 1: file modified; 2: new file; -1: error
	try:
		stp_old = g_file_timestamp.get(filename, None)
		stp_new = os.path.getmtime(filename)
		if stp_old == stp_new:
			return 0
		g_file_timestamp[filename] = stp_new
		return 2 if stp_old is None else 1
	except:
		return -1


class Periodic(object):
	def __init__(self, time_interval):
		self.tm_intv = time_interval
		self.tm_stmp = time.time()

	def __call__(self, interval=None):
		if interval is not None:
			self.tm_intv = interval
		tm = time.time()
		if tm-self.tm_stmp >= self.tm_intv:
			self.tm_stmp = tm
			return True
		return False

