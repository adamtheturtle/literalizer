module Fixture_call_cpp_identity_nested_method_Crystal_call
extend self
class ThingType_; def go(); 0; end; end
class OuterType_; def thing; ThingType_.new; end; end
outer = OuterType_.new
outer.thing.go();
end
