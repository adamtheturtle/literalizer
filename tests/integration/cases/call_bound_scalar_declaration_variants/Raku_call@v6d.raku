sub consume(*@a, *%kw) {}
my $shared = 42;
consume($shared);
