sub consume(*@a, *%kw) {}
my $my_null = Nil;
my $regular_null = Nil;
consume($my_null);
consume($regular_null);
