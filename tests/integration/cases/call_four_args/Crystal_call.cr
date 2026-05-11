module Fixture_call_four_args_Crystal_call
extend self
def process(a = nil, b = nil, c = nil, d = nil); 0; end
process(a: 1, b: 2, c: 3, d: 4);
process(a: 10, b: 20, c: 30, d: 40);
end
