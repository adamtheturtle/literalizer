module Fixture_call_dispatch_transform_Crystal_call
extend self
def record_value(value = nil); 0; end
def flush_buffer(count = nil); 0; end
def emit(_arg = nil); 0; end
emit(record_value(value: 42));
flush_buffer(count: 3);
end
