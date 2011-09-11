#! /usr/bin/perl -w
use strict;
use warnings;
# A program to make sliding window counts of ABBA, BABA, ABBB and BABB patterns across a genomic region
# Last updated on 15 July 2011: Kanchon Dasmahapatra

my $line; my $midpoint; my $i;
my @value; my @position; my @flag;

# Set sliding window step size and window size here
my $step = 1000; my $window = 10000;

my $output_file = $ARGV[0] . '_slide';

open (OUTPUTFILE, ">$output_file");

open INPUTFILE, "$ARGV[0]" or die "could not open input file.\n";
print OUTPUTFILE "Pos\tABBA\tBABA\tABBB\tBABB\tother\tno_data\tABBA_norm\tBABA_norm\tABBB_norm\tBABB_norm\n";

$i = 0;
# Read file into memory
while ($line = <INPUTFILE>) {
	chomp($line);
	@value = split(' ',$line);
	$position[$i] = $value[1];
        $flag[$i] = $value[2];
	$i++
}
close INPUTFILE;

my $nrecords = @position;
my $maxlength = $position[$nrecords - 1];
# print "$maxlength\n";

my $winstart = 0;
my $final = 0;
while ($winstart <= $maxlength - $step) {
	my $ABBAcount = 0; my $BABAcount = 0; my $nodatacount = 0; my $othercount = 0;
	my $ABBBcount = 0; my $BABBcount = 0;
	for ($i = $final; $i < $nrecords; $i++) {
		if ($position[$i] > $winstart + $window) {
			$final = $i - $window;
			if ($final < 0) {
				$final = 0;
			}
			last;
		}
		if ($position[$i] >= $winstart && $position[$i] < $winstart + $window) {
			if ($flag[$i] eq 'no_data') {$nodatacount++;}
			elsif ($flag[$i] eq 'ABBA') {$ABBAcount++;}
			elsif ($flag[$i] eq 'BABA') {$BABAcount++;}
                        elsif ($flag[$i] eq 'BABB') {$BABBcount++;}
                        elsif ($flag[$i] eq 'ABBB') {$ABBBcount++;}
			elsif ($flag[$i] eq 'other' || $flag[$i] eq 'ABBC' || $flag[$i] eq 'BABC' || $flag[$i] eq 'not_ABBA_BABA') {$othercount++;}
			else {print "unknown site category encountered: $position[$i]\n";}
		}
	}				
	close INPUTFILE;
	my $midpoint = $winstart + ($window/2);
        my $ABBA_norm = $ABBAcount/($window-$nodatacount);
        my $BABA_norm = $BABAcount/($window-$nodatacount);
        my $ABBB_norm = $ABBBcount/($window-$nodatacount);
        my $BABB_norm = $BABBcount/($window-$nodatacount);
        print OUTPUTFILE "$midpoint\t$ABBAcount\t$BABAcount\t$ABBBcount\t$BABBcount\t$othercount\t$nodatacount\t$ABBA_norm\t$BABA_norm\t$ABBB_norm\t$BABB_norm\n";
	$winstart = $winstart + $step;
}
close OUTPUTFILE;
