sub process(*@a, *%kw) {}
my $big_list = [
    'x',
];
process({'m' => $big_list});
