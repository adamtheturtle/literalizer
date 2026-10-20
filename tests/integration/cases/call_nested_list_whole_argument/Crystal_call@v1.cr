module Fixture_call_nested_list_whole_argument_Crystal_call
extend self
def f(a = nil); 0; end
f(a: [[1, 2], [3]]);
end
