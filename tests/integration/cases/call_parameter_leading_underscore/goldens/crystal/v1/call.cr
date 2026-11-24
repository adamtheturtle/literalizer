module Fixture_call_parameter_leading_underscore_Crystal_call
extend self
def f(_x = nil); 0; end
f(_x: 1);
end
