
This contains a well-packaged 4 traditional machine-translation evaluation tools: BLEU, NIST, TER and METEOR.

# HOW TO RUN
For English-to-Chinese, run `mteval-en2zh-all-txt-mref.sh` and follow usage
For Chinese-to-English, run `mteval-zh2en-all-txt-mref.sh` and follow usage

For example,
```bash
mteval-en2zh-all-txt-mref.sh en2zh/en2zh.src.txt en2zh/en2zh.1ref.txt en2zh/en2zh.sys.txt
mteval-zh2en-all-txt-mref.sh zh2en/zh2en.src.txt zh2en/zh2en.1ref.txt zh2en/zh2en.sys.txt
```

# HOW TO INSTALL
1. copy all files in ./bin folder into $HOME/bin/

`cp ./bin/* ~/bin/`

2. for BLEU scorer, you need to install perl module XML::Twig

`perl -MCPAN -e 'install XML::Twig'`

3. for METEOR scorer (the binary is downloaded from http://www.cs.cmu.edu/~alavie/METEOR/download/meteor-1.5.tar.gz), you need to copy data/ folder into $HOME/bin/

`cp -rf meteor-1.5/data ~/bin/`

4. append the following 5 lines to $HOME/.bashrc if they are absent
```bash
export PERL5LIB="$HOME/perl5/lib/perl5"
export PERL_LOCAL_LIB_ROOT="$HOME/perl5"
export PERL_MB_OPT="--install_base \"$HOME/perl5\""
export PERL_MM_OPT="INSTALL_BASE=$HOME/perl5"
export PATH="$HOME/perl5/bin:$PATH"
```
