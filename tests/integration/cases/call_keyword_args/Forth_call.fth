: throttler ;
: throttler.check ;
: emit ;
emit(throttler.check(s\" user_1", 1.0e3))
emit(throttler.check(s\" user_2", 2.0005e3))
