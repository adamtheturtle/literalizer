module Fixture_call_whole_empty_list_argument_Crystal_call
extend self
def f(a = nil); 0; end
f(a: [] of Nil);
end
