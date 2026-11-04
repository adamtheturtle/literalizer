module Fixture_call_plain_mixed_empty_arguments_Crystal_sequence_tuple_call
extend self
def make_widget(before = nil, populated = nil, after = nil); 0; end
make_widget(before: Tuple.new, populated: {1}, after: Tuple.new);
make_widget(before: {"text"}, populated: {2}, after: Tuple.new);
make_widget(before: Tuple.new, populated: {"text"}, after: Tuple.new);
make_widget(before: {"text"}, populated: {2}, after: {3});
end
