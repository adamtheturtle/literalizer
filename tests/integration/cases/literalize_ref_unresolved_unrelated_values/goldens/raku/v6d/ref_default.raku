sub consume_widget(*@a, *%kw) {}
my $a = 0;
my $my_data = [
    $a,
    1,
];
consume_widget($my_data);
