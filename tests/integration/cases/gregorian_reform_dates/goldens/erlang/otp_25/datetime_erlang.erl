-module(fixture_gregorian_reform_dates_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "ancient_date" => "1500-03-01",
        "modern_date" => "2024-01-15",
        "before_date" => "1582-10-04",
        "gap_date" => "1582-10-10",
        "transition_date" => "1582-10-15",
        "after_date" => "1582-10-16",
        "before_naive" => {{1582, 10, 4}, {12, 30, 0}},
        "gap_naive" => {{1582, 10, 10}, {12, 30, 0}},
        "transition_positive" => {{1582, 10, 15}, {0, 30, 0}},
        "transition_negative" => {{1582, 10, 15}, {23, 30, 0}},
        "after_positive" => {{1582, 10, 16}, {0, 30, 0}}
    },
    My_data.
