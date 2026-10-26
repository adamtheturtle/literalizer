sub consume_widget(*@a, *%kw) {}
my $item = [];
my $my_data = [
    $item,
    $item,
];
consume_widget($my_data);
