sub process(*@a, *%kw) {}
my $my_var = 42;
my $my_other = 7;
process([$my_var, 42, 'static']);
process([$my_other, 7, 'label']);
