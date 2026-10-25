module Fixture_call_reserved_property_name_Crystal_call
extend self
class FooType_; def class(value = nil); 0; end; end
foo = FooType_.new
foo.class(value: 1);
end
