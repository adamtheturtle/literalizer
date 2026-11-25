module Fixture_record_nested_in_ordered_map_Crystal_record_nested_in_ordered_map
extend self
record Record0, name : Nil, id : Int32
my_data = {
    "outer" => [Record0.new(nil, 1)],
}
end
