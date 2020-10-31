

BLEU=()
NIST=()
TER=()
METEOR=()

for f in $*; do
	BLEU+=(`zcat -f $f | grep '^BLEU ' | tail -1 | awk '{print $2}'`)
	NIST+=(`zcat -f $f | grep '^NIST ' | tail -1 | awk '{print $2}'`)
	TER+=(`zcat -f $f | grep '^TER ' | tail -1 | awk '{print $2}'`)
	METEOR+=(`zcat -f $f | grep '^METEOR ' | tail -1 | awk '{print $2}'`)
done

echo -e "\tBLEU\tNIST\tTER\tMETEOR"
for i in `seq 0 $[${#BLEU[*]}-1]`; do
	echo -e "$i\t${BLEU[i]}\t${NIST[i]}\t${TER[i]}\t${METEOR[i]}"
done

a=`echo ${BLEU[*]} 	| mean.pl`
b=`echo ${NIST[*]} 	| mean.pl`
c=`echo ${TER[*]} 	| mean.pl`
d=`echo ${METEOR[*]} | mean.pl`

echo -e "Average\t$a\t$b\t$c\t$d"

