module Fixture_call_nested_inline_only_Crystal_call
extend self
def f(a = nil, b = nil); 0; end
f(a: 2, b: "hello");  # trailing note
f(a: 3, b: "world");  # another note
end
