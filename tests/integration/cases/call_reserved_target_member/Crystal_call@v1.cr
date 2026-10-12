module Fixture_call_reserved_target_member_Crystal_call
extend self
class ObjType_; def class(a = nil); 0; end; end
obj = ObjType_.new
obj.class(a: 42);
end
