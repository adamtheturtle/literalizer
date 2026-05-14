module Fixture_call_ref_args_reused_Crystal_call
extend self
def process(data = nil, count = nil); 0; end
single_var = [
    4,
    5,
    6,
]
repeated_var = 1
process(data: repeated_var, count: 1);
process(data: single_var, count: 0);
process(data: repeated_var, count: 8);
end
