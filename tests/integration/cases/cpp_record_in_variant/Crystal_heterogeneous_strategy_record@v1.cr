module Fixture_cpp_record_in_variant_Crystal_heterogeneous_strategy_record
extend self
record Record1, k : Array(Bool)
record Record0, h : Array(Array(Int32 | String) | Int32 | String | Nil)
my_data = Record0.new(
    [
        1,
        "a",
        [
            2,
            "b",
        ],
        Record1.new(
            [
                true,
            ],
        ),
    ],
)
end
