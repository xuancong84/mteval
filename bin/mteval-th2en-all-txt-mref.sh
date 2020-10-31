# Usage: $0 src ref sys

set -e
if [ $# != 3 ]; then
	echo "Usage: $0 src.txt mref.txt(.) sys.txt" >&2
	echo "Single reference is in mref.txt" >&2
	echo "Multiple references are in mref.txt.0 mref.txt.1 mref.txt.2 ..." >&2
    exit 1
fi


cat $1 | trim.sh  | txt2xml.sh | wrap-xml.py src zh en >$3.TER-src.xml
if [ "${2:${#2}-1}" == "." ]; then
	wrap-xml.py ref zh en $2 >$3.TER-ref.xml
else
	cat $2 | trim.sh  | txt2xml.sh | wrap-xml.py ref zh en >$3.TER-ref.xml
fi
cat $3 | trim.sh  | txt2xml.sh | wrap-xml.pl $3.TER-src.xml en >$3.TER-sys.xml


# BLEU
echo "BLEU"
mteval-v13a.pl -s $3.TER-src.xml -r $3.TER-ref.xml -t $3.TER-sys.xml | tee $3.BLEU-score


# TER
echo "TER"
java -jar $HOME/bin/tercom.7.25.jar -r $3.TER-ref.xml -h $3.TER-sys.xml | grep -A 3 'Total TER' | tee $3.TER-score


# METEOR
echo "METEOR"
java -Xmx2G -jar $HOME/bin/meteor-1.5.jar $3.TER-sys.xml $3.TER-ref.xml -l en -sgml 2>&1 | tee $3.METEOR-score


echo "All scores:"
bleu=(`cat $3.BLEU-score | grep '^NIST'`)
ter=(`cat $3.TER-score | head -1`)
meteor=(`cat $3.METEOR-score | grep '^Final'`)

echo BLEU ${bleu[7]}
echo NIST ${bleu[3]}
echo TER  ${ter[2]}
echo METEOR ${meteor[2]}

