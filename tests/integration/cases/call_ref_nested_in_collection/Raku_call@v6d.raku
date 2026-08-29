sub process(*@a, *%kw) {}
my $big_list = [
    'x',
];
process({'k' => $big_list}, 2);
