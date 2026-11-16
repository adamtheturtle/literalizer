my @expected_events = 1, 1, 1, 2;
my $event_index = 0;
sub observe_event(Int $actual) {
    die "receiver event changed" unless $event_index < 4 && $actual == @expected_events[$event_index];
    $event_index++;
}
sub process(Int $value) { observe_event(1); observe_event($value); $value + 100 }
sub verify_events() { die "missing receiver events" unless $event_index == 4 }
process(1);
process(2);
verify_events();
