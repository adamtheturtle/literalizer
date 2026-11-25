module Fixture_record_root_nested_map_annotations_Crystal_record_sequence_tuple
extend self
record Record0, x : Int32
my_data = {
    "outer" => { {"inner" => Record0.new(1)},  {"inner" => Record0.new(2)}},
}
end
