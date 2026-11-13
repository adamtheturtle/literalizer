
class Counter {
    has Int $.calls is rw = 0;
    method accept(Str $user, Numeric $timestamp) {
        die "receiver arguments changed" unless $user eq ($!calls == 0 ?? 'user_1' !! 'user_2') && $timestamp == 100 + $!calls;
        $!calls++;
        $user eq 'user_1'
    }
}
my $counter = Counter.new;
my $checks = 0;
sub checkResult($actual, $expected) {
    die "paired result changed" unless $actual == $expected[0] && $expected[1] eq ($checks == 0 ?? 'first' !! 'second');
    $checks++;
}
checkResult($counter.accept('user_1', 100.0e0), [True, 'first']);
checkResult($counter.accept('user_2', 101.0e0), [False, 'second']);
die "calls skipped" unless $counter.calls == 2 && $checks == 2;
