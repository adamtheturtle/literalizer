module Fixture_call_no_params_dotted_Crystal_call
extend self
class ThrottlerType_; def check(); 0; end; end
throttler = ThrottlerType_.new
throttler.check();
throttler.check();
end
