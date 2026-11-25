module Fixture_record_field_type_split_Crystal_record_field_type_split
extend self
record Record1, status : Int32
record Record2, status : String
record Record4, kind : String, urgent : Bool
record Record3, inner : Record4
record Record6, error : String
record Record5, inner : Record6
record Record7, holder : Record1
record Record8, holder : Record2
record Record9, nums : Array(Int32 | Int64)
record Record0, plain : Record1, other : Record2, nested_a : Record3, nested_b : Record5, wrap_a : Record7, wrap_b : Record8, wide : Record9
my_data = Record0.new(
    Record1.new(
        1,
    ),
    Record2.new(
        "ready",
    ),
    Record3.new(
        Record4.new(
            "add",
            true,
        ),
    ),
    Record5.new(
        Record6.new(
            "not_found",
        ),
    ),
    Record7.new(
        Record1.new(
            2,
        ),
    ),
    Record8.new(
        Record2.new(
            "word",
        ),
    ),
    Record9.new(
        [
            1,
            1099511627776,
        ],
    ),
)
end
