sub consume_widget(*@a, *%kw) {}
my $ref_data = [
    1,
    2,
];
my $my_data = [
    0,
];
consume_widget($my_data);
$my_data = $ref_data;
consume_widget($my_data);
