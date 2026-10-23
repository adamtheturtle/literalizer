require "json"
module Fixture_call_zig_helper_member_std_Crystal_json_type_json_any_call
extend self
class ObjType_; def std(value = nil); 0; end; end
obj = ObjType_.new
obj.std(value: JSON.parse(%(1)));
end
