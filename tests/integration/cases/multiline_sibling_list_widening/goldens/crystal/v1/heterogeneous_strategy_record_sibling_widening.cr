module Fixture_multiline_sibling_list_widening_Crystal_heterogeneous_strategy_record_sibling_widening
extend self
record Record1, numbers : Array(Int32), strings : Array(String)
record Record0, omap_value : Hash(String, Int32), sibling_lists : Record1, ref_marker_present : Array(String)
my_data = Record0.new(
    {
        "first" => 1,
    },
    Record1.new(
        [
            1,
            2,
        ],
        [
            "x",
            "y",
        ],
    ),
    [
        "$keep",
        "z",
    ],
)
end
