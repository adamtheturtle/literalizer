module Fixture_record_empty_sibling_arrays_Crystal_heterogeneous_strategy_record_both
extend self
record Record1, item : Int32
record Record2, item : Nil
record Record0, integers : Array(Array(Record1)), nulls : Array(Array(Record2)), nested : Array(Array(Array(Record1))), reversed : Array(Array(Record1))
my_data = Record0.new(
    [
        [] of Record1,
        [
            Record1.new(
                1,
            ),
        ],
    ],
    [
        [] of Record2,
        [
            Record2.new(
                nil,
            ),
        ],
    ],
    [
        [
            [] of Record1,
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
            [] of Record1,
        ],
    ],
    [
        [
            Record1.new(
                4,
            ),
        ],
        [] of Record1,
    ],
)
my_data = Record0.new(
    [
        [] of Record1,
        [
            Record1.new(
                1,
            ),
        ],
    ],
    [
        [] of Record2,
        [
            Record2.new(
                nil,
            ),
        ],
    ],
    [
        [
            [] of Record1,
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
            [] of Record1,
        ],
    ],
    [
        [
            Record1.new(
                4,
            ),
        ],
        [] of Record1,
    ],
)
end
