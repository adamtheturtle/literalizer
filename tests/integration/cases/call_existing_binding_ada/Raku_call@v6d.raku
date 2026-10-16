sub make_widget(*@a, *%kw) {}
my $my_data = make_widget(0);
make_widget($my_data);
$my_data = make_widget(1);
make_widget($my_data);
