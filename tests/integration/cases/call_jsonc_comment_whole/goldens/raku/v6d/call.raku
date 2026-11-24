my @expected_events = 1, 42;
my $event_index = 0;
sub observe_event(Int $actual) {
    die "receiver event changed" unless $event_index < 2 && $actual == @expected_events[$event_index];
    $event_index++;
}
sub f(Int $a) { observe_event(1); observe_event($a); $a + 100 }
sub verify_events() { die "missing receiver events" unless $event_index == 2 }
# scalar heading
# second heading line
# scalar inline
# inline continuation
# scalar trailing
f(42);
verify_events();
