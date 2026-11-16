my @expected_events = 1, 42, 2, 142;
my $event_index = 0;
sub observe_event(Int $actual) {
    die "receiver event changed" unless $event_index < 4 && $actual == @expected_events[$event_index];
    $event_index++;
}
sub make_widget(Int $value) { observe_event(1); observe_event($value); $value + 100 }
sub consume(Int $value) { observe_event(2); observe_event($value) }
sub verify_events() { die "missing receiver events" unless $event_index == 4 }
my $my_data = make_widget(42);
consume($my_data);
verify_events();
