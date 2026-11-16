my @expected_events = 1, 42, 1, 42, 1, 142;
my $event_index = 0;
sub observe_event(Int $actual) {
    die "receiver event changed" unless $event_index < 6 && $actual == @expected_events[$event_index];
    $event_index++;
}
sub make_widget(Int $count) { observe_event(1); observe_event($count); $count + 100 }
sub verify_events() { die "missing receiver events" unless $event_index == 6 }
my $my_data = 42;
make_widget($my_data);
$my_data = make_widget($my_data);
make_widget($my_data);
verify_events();
