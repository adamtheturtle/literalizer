sub throttler {}
sub check {}
sub emit {}
emit(throttler.check("user_1", (0.0 + 1000.0)));
emit(throttler.check("user_2", (0.0 + 2000.5)));
