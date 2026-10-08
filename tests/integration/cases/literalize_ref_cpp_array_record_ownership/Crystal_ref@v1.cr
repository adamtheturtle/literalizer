module Fixture_literalize_ref_cpp_array_record_ownership_Crystal_ref
extend self
record Record1, values : Array(Int32)
record Record2, nested : Array(Array(Int32))
record Record0, trivial : Record1, nested : Record2
trivial = Record1.new(
    [
        1,
        2,
    ],
)
nested = Record2.new(
    [
        [
            1,
            2,
        ],
        [
            3,
            4,
        ],
    ],
)
my_data = Record0.new(
    trivial,
    nested,
)
end
