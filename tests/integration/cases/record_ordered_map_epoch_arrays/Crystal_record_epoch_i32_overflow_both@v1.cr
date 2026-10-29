module Fixture_record_ordered_map_epoch_arrays_Crystal_record_epoch_i32_overflow_both
extend self
record Record0, values : Hash(String, Array(Array(Int32) | Array(Int64)) | Array(Array(Int32)) | Array(Array(Int64)) | String), flag : Bool, direct_arrays : Array(Array(Int64))
my_data = Record0.new(
    {
        "wide" => [
            [
                2208988800,
            ],
            [] of Int64,
        ],
        "narrow" => [
            [
                946684800,
            ],
        ],
        "negative" => [
            [
                -2208988800,
            ],
        ],
        "shifted" => [
            [
                2208988800,
            ],
        ],
        "mixed_width" => [
            [
                946684800,
            ],
            [
                2208988800,
            ],
        ],
        "text" => "preserve",
    },
    true,
    [
        [
            2208988800,
        ],
        [] of Int64,
    ],
)
my_data = Record0.new(
    {
        "wide" => [
            [
                2208988800,
            ],
            [] of Int64,
        ],
        "narrow" => [
            [
                946684800,
            ],
        ],
        "negative" => [
            [
                -2208988800,
            ],
        ],
        "shifted" => [
            [
                2208988800,
            ],
        ],
        "mixed_width" => [
            [
                946684800,
            ],
            [
                2208988800,
            ],
        ],
        "text" => "preserve",
    },
    true,
    [
        [
            2208988800,
        ],
        [] of Int64,
    ],
)
end
