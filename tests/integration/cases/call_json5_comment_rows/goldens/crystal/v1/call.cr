module Fixture_call_json5_comment_rows_Crystal_call
extend self
def f(a = nil, b = nil); 0; end
# calls heading
# before call one
# first argument
f(a: 1, b: 2);  # after call one
# second argument
f(a: 3, b: 4);
# after all calls
end
