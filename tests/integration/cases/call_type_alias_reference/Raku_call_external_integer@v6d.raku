my @expected_events = 1, 1;
my $event_index = 0;
sub observe_event(Int $actual) {
    die "receiver event changed" unless $event_index < 2 && $actual == @expected_events[$event_index];
    $event_index++;
}
sub process(Int $value) { observe_event(1); observe_event($value); $value + 100 }
sub verify_events() { die "missing receiver events" unless $event_index == 2 }
my $value = 1;
process($value);
verify_events();
