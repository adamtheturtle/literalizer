module Fixture_call_multi_args_Crystal_call
extend self
def process(value = nil, count = nil); 0; end
process(value: 1, count: 42);
process(value: 2, count: 100);
end
