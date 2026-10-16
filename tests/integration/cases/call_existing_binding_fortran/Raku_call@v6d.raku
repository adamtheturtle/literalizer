sub make_widget(*@a, *%kw) {}
sub consume_widget(*@a, *%kw) {}
my $my_data = make_widget(0);
consume_widget($my_data);
$my_data = make_widget(1);
consume_widget($my_data);
