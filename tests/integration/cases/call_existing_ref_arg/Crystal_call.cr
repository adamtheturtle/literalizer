module Fixture_call_existing_ref_arg_Crystal_call
extend self
def send(value = nil); 0; end
existing = 42
send(value: existing);
end
