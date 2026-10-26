module Fixture_call_wrapper_outer_Crystal_call
extend self
def process(value = nil); 0; end
def emit(_arg = nil); 0; end
emit(process(value: 42));
end
