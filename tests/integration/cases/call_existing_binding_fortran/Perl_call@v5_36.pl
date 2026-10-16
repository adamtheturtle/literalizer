sub make_widget {}
sub consume_widget {}
my $my_data = make_widget(0);
consume_widget($my_data);
$my_data = make_widget(1);
consume_widget($my_data);
