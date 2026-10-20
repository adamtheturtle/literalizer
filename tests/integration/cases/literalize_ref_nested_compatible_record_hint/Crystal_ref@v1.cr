module Fixture_literalize_ref_nested_compatible_record_hint_Crystal_ref
extend self
record Record1, items : Array(Int32)
record Record0, outer : Record1
record_data = Record1.new(
    [
        1,
        2,
    ],
)
my_data = Record0.new(
    record_data,
)
end
