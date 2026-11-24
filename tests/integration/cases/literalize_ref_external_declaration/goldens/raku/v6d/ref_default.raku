sub consume_widget(*@a, *%kw) {}
my $shared = [
    1,
    2,
];
my $my_data = $shared;
consume_widget($my_data);
