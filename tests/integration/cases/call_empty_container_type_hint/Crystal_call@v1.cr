module Fixture_call_empty_container_type_hint_Crystal_call
extend self
def process(values = nil, count = nil); 0; end
process(values: [1, {} of String => String], count: 42);
end
