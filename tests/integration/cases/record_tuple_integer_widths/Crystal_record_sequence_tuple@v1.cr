module Fixture_record_tuple_integer_widths_Crystal_record_sequence_tuple
extend self
record Record0, narrow_pair : Tuple(Int32, Int32), wide_pair : Tuple(Int32, Int64), wide_triple : Tuple(Int32, Int32, Int64), beyond_pair : Tuple(Int32, Int128), beyond_triple : Tuple(Int32, Int32, Int128), mixed_triple : Tuple(Int32, String, Bool)
my_data = Record0.new(
    {
        1,
        2,
    },
    {
        1,
        1099511627776,
    },
    {
        1,
        2,
        1099511627776,
    },
    {
        1,
        18446744073709551616_i128,
    },
    {
        1,
        2,
        18446744073709551616_i128,
    },
    {
        1,
        "text",
        true,
    },
)
end
