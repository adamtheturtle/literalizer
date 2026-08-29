sub process(*@a, *%kw) {}
my $big_list = [
    'x',
];
process({'k' => $big_list}, {'m' => $big_list});
