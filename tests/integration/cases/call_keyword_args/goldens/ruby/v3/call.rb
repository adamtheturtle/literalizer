class ThrottlerType; def check(*a, **kw); end; end
throttler = ThrottlerType.new
def emit(*a); end
emit(throttler.check(user_id: "user_1", ts: 1000.0))
emit(throttler.check(user_id: "user_2", ts: 2000.5))
