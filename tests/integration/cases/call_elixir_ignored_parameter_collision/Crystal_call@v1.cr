module Fixture_call_elixir_ignored_parameter_collision_Crystal_call
extend self
def f(x = nil, _x = nil); 0; end
f(x: 1, _x: 2);
end
