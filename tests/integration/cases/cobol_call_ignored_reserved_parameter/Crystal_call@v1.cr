module Fixture_cobol_call_ignored_reserved_parameter_Crystal_call
extend self
def process(count = nil); 0; end
process(count: 42);
end
