module Fixture_literalize_ref_record_array_compatible_hint_Crystal_ref
extend self
record Record0, items : Array(Int32)
record_data = [
    Record0.new([1, 2]),
]
my_data = record_data
end
