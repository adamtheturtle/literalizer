require "json"
module Fixture_call_nim_plain_mixed_empty_arguments_Crystal_json_type_json_any_call
extend self
def make_widget(before = nil, populated = nil, after = nil); 0; end
make_widget(before: JSON.parse(%([])), populated: JSON.parse(%([1])), after: JSON.parse(%([])));
make_widget(before: JSON.parse(%(["text"])), populated: JSON.parse(%([2])), after: JSON.parse(%([])));
make_widget(before: JSON.parse(%([])), populated: JSON.parse(%(["text"])), after: JSON.parse(%([])));
make_widget(before: JSON.parse(%(["text"])), populated: JSON.parse(%([2])), after: JSON.parse(%([3])));
end
