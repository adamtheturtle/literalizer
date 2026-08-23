module Fixture_call_self_target_Crystal_call
extend self
def self(value = nil); 0; end
self(value: "hello");
end
