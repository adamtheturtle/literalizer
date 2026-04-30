module Fixture_call_ref_args_reused_Crystal_call
extend self
def process(data = nil, count = nil); 0; end
shared = 1
other = 2
process(data: shared, count: 1);
process(data: other, count: 0);
process(data: shared, count: 8);
end
