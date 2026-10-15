module Fixture_literalize_ref_empty_record_sequence_Crystal_ref
extend self
record Record0, x : Int32
empty_items = [] of Hash(String, Int32)
populated_items = [
    Record0.new(1),
]
my_data = [
    empty_items,
    populated_items,
]
end
