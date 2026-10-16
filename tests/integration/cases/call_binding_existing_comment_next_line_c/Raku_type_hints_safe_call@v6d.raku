sub make_widget(*@a, *%kw) {}
my $my_data = make_widget(42);
make_widget($my_data);
$my_data = make_widget($my_data)
// note;
make_widget($my_data);
