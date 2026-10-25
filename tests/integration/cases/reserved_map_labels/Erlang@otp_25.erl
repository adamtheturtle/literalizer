-module(fixture_reserved_map_labels_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "if" => 1,
        "then" => 2,
        "else" => 3,
        "let" => 4,
        "in" => 5,
        "using" => 6,
        "missing" => 7,
        "assert" => 8,
        "as" => 9,
        "Infinity" => 10,
        "NaN" => 11,
        "merge" => 12,
        "Some" => 13,
        "toMap" => 14,
        "forall" => 15,
        "with" => 16,
        "ordinary" => 17
    },
    My_data.
