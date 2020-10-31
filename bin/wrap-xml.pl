#!/usr/bin/perl -w

use strict;

my $src = $ARGV[0];
my $language = $ARGV[1];
die("syntax: wrap-xml.pl xml-frame language [system-name]") 
    unless $src && $language && -e $src;
my $system = "my-system";
$system = $ARGV[2] if defined($ARGV[2]);

open(SRC,$src);
my @OUT = <STDIN>;
chomp(@OUT);
#print $OUT[0]."\n";

#my @OUT = `cat $decoder_output`;
while(<SRC>) {
    chomp;
    if (/^<srcset/) { 
		s/<srcset/<tstset/;
		s/trglang=".."/trglang="$language"/;
		s/>/ sysid="mysystem">/;
    }
    elsif (/^<\/srcset/) {
		s/<\/srcset/<\/tstset/;
    }
    elsif (/^<DOC/) {
		if (! /sysid=/){
			s/<DOC/<DOC sysid="$system"/;
		}
    }
    elsif (/<seg/) {
		my $line = shift(@OUT);
        $line = "" if $line =~ /NO BEST TRANSLATION/;
        if (/<\/seg>/) {
			s/(<seg[^>]+> *).+(<\/seg>)/$1$line$2/;
        }
        else {
			s/(<seg[^>]+> *)[^<]+/$1$line/;
        }
    }
    print $_."\n";
}
