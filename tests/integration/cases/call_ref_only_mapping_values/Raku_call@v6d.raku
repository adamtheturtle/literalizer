sub consume(*@a, *%kw) {}
my $item = 42;
consume({'field' => $item});
