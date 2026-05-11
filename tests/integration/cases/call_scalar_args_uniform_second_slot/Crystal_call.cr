module Fixture_call_scalar_args_uniform_second_slot_Crystal_call
extend self
def process(value = nil, label = nil); 0; end
process(value: "hello", label: "a");
process(value: 42, label: "b");
process(value: true, label: "c");
end
