class ThrottlerType_; def check(*a, **kw); 0; end; end
throttler = ThrottlerType_.new
def emit(*a, **kw); 0; end
emit(throttler.check("user_1", 1000.0));
emit(throttler.check("user_2", 2000.5));
