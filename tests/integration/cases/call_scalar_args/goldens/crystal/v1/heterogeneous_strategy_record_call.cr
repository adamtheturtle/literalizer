module Fixture_call_scalar_args_Crystal_heterogeneous_strategy_record_call
extend self
def process(value = nil); 0; end
process(value: "hello");
process(value: 42);
process(value: true);
end
