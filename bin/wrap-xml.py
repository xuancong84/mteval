#!/usr/bin/env python2

import os
execfile(os.getenv('HOME')+'/bin/NLP.py')

if len(sys.argv)==1:
	print >>sys.stderr, 'Usage: $0 src|ref srclang trglang [multi-ref-prefix-including-dot] <input >output'
	print >>sys.stderr, 'Multiple references are in multi-ref-prefix.0 multi-ref-prefix.1 ...'
	print >>sys.stderr, 'You can also put single reference at multi-ref-prefix for escaping XML characters, as no XML-character escaping will be done on STDIN'
	sys.exit(1)

xml_type=sys.argv[1]+'set'
src_lang=sys.argv[2]
trg_lang=sys.argv[3]

def escapeXML(L):
	return ' '.join(L.split()).replace('<','&lt;').replace('&','&amp;')

def noescapeXML(L):
	return ' '.join(L.split())

# load all references
data=[]
if len(sys.argv)<=4:
	data+=[[noescapeXML(L) for L in sys.stdin.readlines()]]
else:
	if os.path.isfile(sys.argv[4]):
		data+=[[escapeXML(L) for L in open(sys.argv[4]+str(i))]]
	else:
		i=0
		while os.path.isfile(sys.argv[4]+str(i)):
			data+=[[escapeXML(L) for L in open(sys.argv[4]+str(i))]]
			i+=1


# Write output XML
print '<?xml version="1.0" encoding="UTF-8"?>'
print '<mteval>'


for i,datum in enumerate(data):
	print '<'+xml_type,'setid="set"', 'srclang="'+src_lang+'"', 'trglang="'+trg_lang+'"', 'refid="reference_'+str(i+1)+'">'
	print '<doc docid="document1">'

	for id,L in enumerate(datum):
		print '<seg id="'+str(id+1)+'">', L, '</seg>'

	print '</doc>'
	print '</'+xml_type+'>'

print '</mteval>'

