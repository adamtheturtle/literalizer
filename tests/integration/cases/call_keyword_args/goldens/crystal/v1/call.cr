module Fixture_call_keyword_args_Crystal_call
extend self
class ThrottlerType_; def check(user_id = nil, ts = nil); 0; end; end
throttler = ThrottlerType_.new
def emit(_arg = nil); 0; end
emit(throttler.check(user_id: "user_1", ts: 1000.0));
emit(throttler.check(user_id: "user_2", ts: 2000.5));
end
