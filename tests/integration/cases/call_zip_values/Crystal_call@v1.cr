module Fixture_call_zip_values_Crystal_call
extend self
def process(value = nil); 0; end
def emit(_call = nil, _zip = nil); 0; end
emit(process(value: "hello"), true);
emit(process(value: 42), false);
end
