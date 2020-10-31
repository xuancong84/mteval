set -e -o pipefail

pycode="
import os,sys

s_set='<'+sys.argv[1]
s_id=sys.argv[2]+'='

ii=1
if len(sys.argv)>3:
	print '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'
	print '<mteval>'

for L in sys.stdin:
	if L.startswith(s_set):
		its=L.strip().split()
		if L.find('setid=')<0:
			its[0]+=' setid=\"set\"'
		if L.find(s_id)<0:
			its[0]+=(' '+s_id+'\"reference_'+str(ii)+'\"')
			ii+=1
		print ' '.join(its)
	else:
		print L.strip()
	
if len(sys.argv)>3:
	print '</mteval>'
"

sed "s:^<seg id=\([0-9][0-9]*\):<seg id=\"\1\":g; s:^<DOC:<doc:g; s:^</DOC:</doc:g; /^<?xml/d; /^<mteval/d; /^<\/mteval/d" \
	| python -c "$pycode" refset refid \
	| python -c "$pycode" tstset sysid \
	| python -c "$pycode" srcset srcid 1

