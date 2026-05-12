module Fixture_call_scalar_args_with_null_Crystal_call
extend self
def process(value = nil); 0; end
process(value: nil);
process(value: "hello");
end
