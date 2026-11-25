sub make_widget {}
sub consume {}
my $my_data = make_widget(undef);
consume($my_data);
$my_data = make_widget(42);
consume($my_data);
