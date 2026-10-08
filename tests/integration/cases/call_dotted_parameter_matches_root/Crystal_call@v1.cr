module Fixture_call_dotted_parameter_matches_root_Crystal_call
extend self
class OuterType_; def inner(outer = nil, n = nil); 0; end; end
outer = OuterType_.new
outer.inner(outer: 1, n: 2);
end
