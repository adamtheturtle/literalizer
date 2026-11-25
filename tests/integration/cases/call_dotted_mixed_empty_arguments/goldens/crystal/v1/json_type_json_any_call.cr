require "json"
module Fixture_call_dotted_mixed_empty_arguments_Crystal_json_type_json_any_call
extend self
class ThingType_; def go(before = nil, populated = nil, after = nil); 0; end; end
thing = ThingType_.new
thing.go(before: JSON.parse(%([])), populated: JSON.parse(%([1])), after: JSON.parse(%([])));
thing.go(before: JSON.parse(%(["text"])), populated: JSON.parse(%([2])), after: JSON.parse(%([])));
thing.go(before: JSON.parse(%([])), populated: JSON.parse(%(["text"])), after: JSON.parse(%([])));
thing.go(before: JSON.parse(%(["text"])), populated: JSON.parse(%([2])), after: JSON.parse(%([3])));
end
