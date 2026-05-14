sub process(*@a, *%kw) {}
my $single_var = [
    4,
    5,
    6,
];
my $repeated_var = 1;
process($repeated_var, 1);
process($single_var, 0);
process($repeated_var, 8);
