module Fixture_call_null_and_array_arguments_Crystal_call
extend self
def process(value = nil); 0; end
process(value: nil);
process(value: [1, 2]);
end
