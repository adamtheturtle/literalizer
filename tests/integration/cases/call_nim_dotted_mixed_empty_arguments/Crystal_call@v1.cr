module Fixture_call_nim_dotted_mixed_empty_arguments_Crystal_call
extend self
class ThingType_; def go(before = nil, populated = nil, after = nil); 0; end; end
thing = ThingType_.new
thing.go(before: [] of Nil, populated: [1], after: [] of Nil);
thing.go(before: ["text"], populated: [2], after: [] of Nil);
thing.go(before: [] of Nil, populated: ["text"], after: [] of Nil);
thing.go(before: ["text"], populated: [2], after: [3]);
end
