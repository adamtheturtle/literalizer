sub consume_widget(*@a, *%kw) {}
my $item = Nil;
my $my_data = Nil;
consume_widget($my_data);
$my_data = $item;
consume_widget($my_data);
