sub process(*@a, *%kw) {}
my $my_var = 42;
process({'key' => $my_var, 'count' => 42});
