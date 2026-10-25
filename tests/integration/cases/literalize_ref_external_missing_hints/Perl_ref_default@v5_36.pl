sub consume_widget {}
my $item = [
    1,
    2,
];
my $my_data = [
    1,
    2,
];
consume_widget($my_data);
$my_data = $item;
consume_widget($my_data);
