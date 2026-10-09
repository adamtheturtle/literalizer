module Fixture_call_cpp_identity_bound_method_Crystal_call
extend self
class ThingType_; def go(value = nil); 0; end; end
thing = ThingType_.new
item = [
    1,
    2,
]
thing.go(value: item);
end
