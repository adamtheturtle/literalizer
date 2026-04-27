module Check
extend self
class ThrottlerType_; def check(user_id = nil, ts = nil); 0; end; end
throttler = ThrottlerType_.new
def emit(_arg = nil); 0; end
emit(throttler.check("user_1", 1000.0));
emit(throttler.check("user_2", 2000.5));
end
