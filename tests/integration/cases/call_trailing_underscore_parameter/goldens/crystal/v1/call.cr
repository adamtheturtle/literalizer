module Fixture_call_trailing_underscore_parameter_Crystal_call
extend self
def do_thing(x_ = nil); 0; end
do_thing(x_: 1);
do_thing(x_: 2);
end
