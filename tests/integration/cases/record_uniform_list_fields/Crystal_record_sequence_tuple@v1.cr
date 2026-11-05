module Fixture_record_uniform_list_fields_Crystal_record_sequence_tuple
extend self
record Record0, scores : Tuple(Int32, Int32)
my_data = {
    Record0.new({1, 2}),
    Record0.new({3, 4}),
}
end
