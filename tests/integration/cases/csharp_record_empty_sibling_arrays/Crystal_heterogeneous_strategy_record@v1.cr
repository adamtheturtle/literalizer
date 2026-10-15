module Fixture_csharp_record_empty_sibling_arrays_Crystal_heterogeneous_strategy_record
extend self
record Record1, item : Int32
record Record2, item : Nil
record Record0, integers : Array(Array(Nil)), nulls : Array(Array(Nil)), nested : Array(Array(Array(Nil))), reversed : Array(Array(Nil))
my_data = Record0.new(
    [
        [] of Hash(String, Int32),
        [
            Record1.new(
                1,
            ),
        ],
    ],
    [
        [] of Hash(String, String),
        [
            Record2.new(
                nil,
            ),
        ],
    ],
    [
        [
            [] of Hash(String, Int32),
            [
                Record1.new(
                    2,
                ),
            ],
        ],
        [
            [
                Record1.new(
                    3,
                ),
            ],
            [] of Hash(String, Int32),
        ],
    ],
    [
        [
            Record1.new(
                4,
            ),
        ],
        [] of Hash(String, Int32),
    ],
)
end
