module Fixture_call_parameter_trailing_underscore_Crystal_call
extend self
def f(x_ = nil); 0; end
f(x_: 1);
end
