sub process(*@a, *%kw) {}
my $my_var = 42;
my $my_other = 7;
process([{'ref' => 'my_var'}, 42, 'static']);
process([{'ref' => 'my_other'}, 7, 'label']);
