module Fixture_call_dispatch_Crystal_call
extend self
def store_item(key = nil, value = nil); 0; end
def read_item(key = nil); 0; end
store_item(key: 1, value: 10);
read_item(key: 1);
end
