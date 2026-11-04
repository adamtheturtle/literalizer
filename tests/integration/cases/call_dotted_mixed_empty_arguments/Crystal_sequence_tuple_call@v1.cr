module Fixture_call_dotted_mixed_empty_arguments_Crystal_sequence_tuple_call
extend self
class ThingType_; def go(before = nil, populated = nil, after = nil); 0; end; end
thing = ThingType_.new
thing.go(before: Tuple.new, populated: {1}, after: Tuple.new);
thing.go(before: {"text"}, populated: {2}, after: Tuple.new);
thing.go(before: Tuple.new, populated: {"text"}, after: Tuple.new);
thing.go(before: {"text"}, populated: {2}, after: {3});
end
