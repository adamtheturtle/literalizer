sub process(*@a, *%kw) {}
my $my_var = [
    1,
    2,
    3,
];
my $my_other = [
    4,
    5,
    6,
];
process($my_var, 42);
process($my_other, 7);
