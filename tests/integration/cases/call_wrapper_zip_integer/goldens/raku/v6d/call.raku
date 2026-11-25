my @expected_events = 1, 1, 2, 101, 3, 42;
my $event_index = 0;
sub observe_event(Int $actual) {
    die "receiver event changed" unless $event_index < 6 && $actual == @expected_events[$event_index];
    $event_index++;
}
sub process(Int $value) { observe_event(1); observe_event($value); $value + 100 }
sub emit(Int $actual, Int $zipped) { observe_event(2); observe_event($actual); observe_event(3); observe_event($zipped) }
sub verify_events() { die "missing receiver events" unless $event_index == 6 }
emit(process(1), 42);
verify_events();
