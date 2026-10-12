sub make_widget(*@a, *%kw) {}
my $my_data = 42;
$my_data = make_widget(42) // note;
