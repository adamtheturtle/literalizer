module Fixture_call_bound_ref_transform_Crystal_call
extend self
def f(a = nil); 0; end
ref_data = 1
f(a: ref_data);
end
