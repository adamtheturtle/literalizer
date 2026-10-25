sub consume_widget(*@a, *%kw) {}
my $missing = [
    1,
    2,
];
my $my_data = $missing;
consume_widget($my_data);
