module Fixture_call_nested_inline_between_comments_Crystal_call
extend self
def f(a = nil, b = nil); 0; end
f(a: 2, b: "hello");  # trailing note
# next element
f(a: 3, b: "world");
end
