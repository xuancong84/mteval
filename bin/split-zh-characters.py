#!/usr/bin/env python2

import os,sys

while True:
	L=sys.stdin.readline()
	if L=='':
		break
	chars=[c for c in ' '.join(L.split()).decode('utf8','ignore')]
	chars=[(c if ord(c)<1270 else ' '+c+' ') for c in chars]
	print ' '.join(''.join(chars).split()).encode('utf8')
	sys.stdout.flush()

