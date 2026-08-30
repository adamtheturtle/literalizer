module Fixture_call_nested_inline_middle_Crystal_call
extend self
def f(ops = nil); 0; end
f(ops: [["DEL", "b", "10"], ["ADD", "a", "x"]]);  # note
end
