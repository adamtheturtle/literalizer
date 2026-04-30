sub process(*@a, *%kw) {}
my $shared = 1;
my $other = 2;
process($shared, 1);
process($other, 0);
process($shared, 8);
