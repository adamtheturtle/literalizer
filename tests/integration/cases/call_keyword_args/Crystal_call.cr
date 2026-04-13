class ThrottlerType_; def check(*a, **kw); 0; end; end
throttler = ThrottlerType_.new
def emit(*a, **kw); 0; end
emit(throttler.check(user_id: "user_1", ts: 1000.0));
emit(throttler.check(user_id: "user_2", ts: 2000.5));
